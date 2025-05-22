How to start?
1. Configure your API KEY in the .env file.
2. ```uv run client.py server.py```

Use Anthropic to test your mcp server
```
npx -y @modelcontextprotocol/inspector uv run server.py
```

示例：
```iterm
🤖 MCP 客户端已启动！输入 'quit' 退出

你: 获取600519的年报
Processing request of type ListToolsRequest

 第一次调用模型返回： ChatCompletion(id='f56a9be8-947f-4a3e-8806-eb6a5eec4586', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content='', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_0_6c8739df-0193-4613-a6b2-0cf914292cf3', function=Function(arguments='{"code":"600519"}', name='getReports'), type='function', index=0)]))], created=1747892349, model='deepseek-chat', object='chat.completion', service_tier=None, system_fingerprint='fp_8802369eaa_prod0425fp8', usage=CompletionUsage(completion_tokens=19, prompt_tokens=166, total_tokens=185, completion_tokens_details=None, prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=128), prompt_cache_hit_tokens=128, prompt_cache_miss_tokens=38))

content: Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content='', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_0_6c8739df-0193-4613-a6b2-0cf914292cf3', function=Function(arguments='{"code":"600519"}', name='getReports'), type='function', index=0)]))
Processing request of type CallToolRequest


[Calling tool getReports with args {'code': '600519'}]



🤖 OpenAI: 以下是贵州茅台（600519）近年年度报告的下载链接，按年份分类整理：

### 2024年
- **年报摘要**: [下载PDF](https://www.sse.com.cn/disclosure/listedinfo/announcement/c/new/2025-04-03/600519_20250403_DQRN.pdf)
- **完整年报**: [下载PDF](https://www.sse.com.cn/disclosure/listedinfo/announcement/c/new/2025-04-03/600519_20250403_QVTI.pdf)

### 2023年
- **年报摘要**: [下载PDF](https://www.sse.com.cn/disclosure/listedinfo/announcement/c/new/2024-04-03/600519_20240403_IU3U.pdf)
- **完整年报**: [下载PDF](https://www.sse.com.cn/disclosure/listedinfo/announcement/c/new/2024-04-03/600519_20240403_W0YD.pdf)

### 2022年
- **年报摘要**: [下载PDF](https://www.sse.com.cn/disclosure/listedinfo/announcement/c/new/2023-03-31/600519_20230331_HPY9.pdf)
- **完整年报**: [下载PDF](https://www.sse.com.cn/disclosure/listedinfo/announcement/c/new/2023-03-31/600519_20230331_O0A1.pdf)

### 其他相关文件
如需2021年及之前的年报、ESG报告、审计报告等，可通过上方数据中的链接下载。

**提示**：
1. 部分链接需在上交所官网验证后下载，若无法直接打开，建议访问[上交所披露页面](https://www.sse.com.cn/)，搜索代码“600519”获取。
2. 2024年报告为示例数据（实际需待公司正式发布）。

如需进一步处理（如数据提取或分析），请告知具体需求。

你: 下载2024年完整年报到本地/Users/xiangguangye/workspace/python/mcp_test/mcp-client
Processing request of type ListToolsRequest


 第一次调用模型返回： ChatCompletion(id='7d0a6198-1972-45e4-88e5-45b3dd687404', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content='', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_0_bd804ea5-53c1-438a-a601-af88dc7f46d6', function=Function(arguments='{"url":"https://www.sse.com.cn/disclosure/listedinfo/announcement/c/new/2025-04-03/600519_20250403_QVTI.pdf","file_path":"/Users/xiangguangye/workspace/python/mcp_test/mcp-client"}', name='savePdfWithUrl'), type='function', index=0)]))], created=1747892416, model='deepseek-chat', object='chat.completion', service_tier=None, system_fingerprint='fp_8802369eaa_prod0425fp8', usage=CompletionUsage(completion_tokens=78, prompt_tokens=2139, total_tokens=2217, completion_tokens_details=None, prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=128), prompt_cache_hit_tokens=128, prompt_cache_miss_tokens=2011))

content: Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content='', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_0_bd804ea5-53c1-438a-a601-af88dc7f46d6', function=Function(arguments='{"url":"https://www.sse.com.cn/disclosure/listedinfo/announcement/c/new/2025-04-03/600519_20250403_QVTI.pdf","file_path":"/Users/xiangguangye/workspace/python/mcp_test/mcp-client"}', name='savePdfWithUrl'), type='function', index=0)]))
Processing request of type CallToolRequest


[Calling tool savePdfWithUrl with args {'url': 'https://www.sse.com.cn/disclosure/listedinfo/announcement/c/new/2025-04-03/600519_20250403_QVTI.pdf', 'file_path': '/Users/xiangguangye/workspace/python/mcp_test/mcp-client'}]



🤖 OpenAI: 贵州茅台2024年完整年报已成功下载至本地路径：
`/Users/xiangguangye/workspace/python/mcp_test/mcp-client/600519_20250403_QVTI.pdf`

如需进一步处理（如解析PDF内容或分析数据），请告知具体需求。

你: Processing request of type ListToolsRequest

 第一次调用模型返回： ChatCompletion(id='074107f4-e8ba-44a1-be49-f5985e6bdffd', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='贵州茅台2024年完整年报已成功下载到以下路径：  \n`/Users/xiangguangye/workspace/python/mcp_test/mcp-client/600519_20250403_QVTI.pdf`\n\n如果需要对该PDF文件进行解析、数据分析或其他操作，请告诉我具体需求，我可以进一步协助你。', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=None))], created=1747892435, model='deepseek-chat', object='chat.completion', service_tier=None, system_fingerprint='fp_8802369eaa_prod0425fp8', usage=CompletionUsage(completion_tokens=67, prompt_tokens=2319, total_tokens=2386, completion_tokens_details=None, prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=2176), prompt_cache_hit_tokens=2176, prompt_cache_miss_tokens=143))

content: Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='贵州茅台2024年完整年报已成功下载到以下路径：  \n`/Users/xiangguangye/workspace/python/mcp_test/mcp-client/600519_20250403_QVTI.pdf`\n\n如果需要对该PDF文件进行解析、数据分析或其他操作，请告诉我具体需求，我可以进一步协助你。', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=None))

🤖 OpenAI: 贵州茅台2024年完整年报已成功下载到以下路径：
`/Users/xiangguangye/workspace/python/mcp_test/mcp-client/600519_20250403_QVTI.pdf`

如果需要对该PDF文件进行解析、数据分析或其他操作，请告诉我具体需求，我可以进一步协助你。

你:
```


doc : https://deepseek.csdn.net/67e28cf28393e26e265938ce.html
