# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2025/4/16 12:26

@desc: mcp客户端，支持历史消息

'''

import asyncio
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
from contextlib import AsyncExitStack
import json
from typing import Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import traceback
import uuid

# 加载 .env 文件，确保 API Key 受到保护
load_dotenv()


class AppLogger:
    def __init__(self):
        """Initialize the logger with a file that will be cleared on startup."""
        self.log_file = "model.log"
        # Clear the log file on startup
        with open(self.log_file, 'w') as f:
            f.write("")

    def log(self, message):
        """Log a message to both file and console."""

        # Log to file
        with open(self.log_file, 'a') as f:
            f.write(message + "\n")


logger = AppLogger()


class MCPClient:
    def __init__(self):
        """初始化 MCP 客户端"""
        self.exit_stack = AsyncExitStack()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")  # 读取 OpenAI API Key
        self.base_url = os.getenv("OPENAI_BASE_URL")  # 读取 BASE YRL
        self.model = os.getenv("OPENAI_MODEL")  # 读取 model

        if not self.openai_api_key:
            raise ValueError("❌ 未找到 OpenAI API Key，请在 .env 文件中设置 OPENAI_API_KEY")

        self.client = OpenAI(api_key=self.openai_api_key, base_url=self.base_url)
        self.session: Optional[ClientSession] = None
        self.history = []
        self.tools = []

    async def connect_to_server(self, server_script_path: str):
        """连接到 MCP 服务器并列出可用工具"""
        logger.log(f"server_script_path:{server_script_path}")
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("服务器脚本必须是 .py 或 .js 文件")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        # 启动 MCP 服务器并建立通信
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # 列出 MCP 服务器上的工具
        response = await self.session.list_tools()
        tools = response.tools
        logger.log(f"已连接到服务器，支持以下工具:{[tool.name for tool in tools]}")
        available_tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
        } for tool in response.tools]
        self.tools = available_tools

    async def process_query(self, query: str) -> str:
        global trace_id
        trace_id = uuid.uuid4()
        """
        使用大模型处理查询并调用可用的 MCP 工具 (Function Calling)
        """
        self.history.append({"role": "user", "content": query})

        response = self.call_model(add_tools=True)

        # 处理返回的内容
        content = response.choices[0]
        self.history.append(content.message.model_dump())
        if content.finish_reason == "tool_calls":
            # 如何是需要使用工具，就解析工具
            tool_call = content.message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            # 执行工具
            result = await self.session.call_tool(tool_name, tool_args)
            logger.log(f"【traceId:{trace_id}】-[Calling tool {tool_name} with args {tool_args}]")

            # 将模型返回的调用哪个工具数据和工具执行完成后的数据都存入messages中
            self.history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": result.content[0].text
            })
            # 将上面的结果再返回给大模型用于生产最终的结果
            response = self.call_model()
            self.history.append(response.choices[0].message)
            return response.choices[0].message.content

        return content.message.content

    def call_model(self, add_tools=False):
        if add_tools == True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                tools=self.tools
            )
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
            )
        logger.log(f"【traceId:{trace_id}】-模型请求：\n{json.dumps(self.history, indent=2, ensure_ascii=False)}")
        logger.log(f"【traceId:{trace_id}】-模型响应：\n{json.dumps(response.model_dump_json(), indent=2, ensure_ascii=False)}")
        return response

    async def chat_loop(self):
        """运行交互式聊天循环"""
        print("\n🤖 MCP 客户端已启动！输入 'quit' 退出")

        while True:
            try:
                query = input("\n你: ").strip()
                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)  # 发送用户输入到 OpenAI API
                logger.log(
                    f"【traceId:{trace_id}】-打印历史消息：\n{json.dumps(self.history, indent=2, ensure_ascii=False)}")
                print(f"\n🤖 OpenAI: {response}")

            except Exception as e:
                print(f"\n⚠️ 发生错误: {str(e)}")
                traceback.print_exc()

    async def cleanup(self):
        """清理资源"""
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        logger.log("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
