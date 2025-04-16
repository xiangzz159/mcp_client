import time

from mcp.server.fastmcp import FastMCP
import datetime
import requests
import json
import urllib.request
import random

# Create an MCP server
mcp = FastMCP('获取A股上司公司年报')

@mcp.tool()
def getReports(code: int) -> dict:
    """根据股票代码查询最近5年的公告
    :param code: 上司公司股票代码
    :return: 返回5年公告信息
    """
    result = {}
    if code[0] == '6':
        result = get_report_list_sh(str(code))
    else:
        result = get_report_list_sz(str(code))

    return result


@mcp.tool()
def savePdfWithUrl(url: str, file_path: str) -> str:
    """通过url下载文件到本地
    :param url: 文件下载路径
    :param file_path: 本地文件保存路径
    :return:
    """
    if file_path[-1] != '/':
        file_path += '/'
    save_path = file_path + url.split('/')[-1]
    try:
        urllib.request.urlretrieve(url, save_path)
        return f'下载成功:{save_path}'
    except Exception as e:
        return f'下载失败：{e}'


def get_report_list_sz(code: str):
    """
    获取深圳上市公司5年公告
    :param url: 股票代码
    :return: 年报pdf下载列表
    """
    nowTime = datetime.datetime.now()
    endDate = time.strftime('%Y-%m-%d', time.localtime())
    lastTime = nowTime + datetime.timedelta(days=-5 * 365)
    beginDate = lastTime.strftime('%Y-%m-%d')
    url = f'https://www.szse.cn/api/disc/announcement/annList?random={random.random()}'
    payload = json.dumps({
        'seDate': [
            beginDate,
            endDate
        ],
        'stock': [
            code
        ],
        'channelCode': [
            'fixed_disc'
        ],
        'pageSize': 50,
        'pageNum': 1
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request('POST', url, headers=headers, data=payload)

    result = json.loads(response.text)
    data = result['data']
    result = []
    for info in data:
        result.append({
            '标题': info['title'],
            '下载路径': 'https://disc.static.szse.cn/download' + info['attachPath']
        })
    return {'responseCode': '000000', 'responseMsg': 'Success', 'data': result}

def get_report_list_sh(code: str):
    """
    获取上海上司公司5年公告
    :param url: 股票代码
    :return:年报pdf下载列表
    """
    ts = int(time.time() * 1000)
    nowTime = datetime.datetime.now()
    endDate = time.strftime('%Y-%m-%d', time.localtime())
    lastTime = nowTime + datetime.timedelta(days=-5 * 365)
    beginDate = lastTime.strftime('%Y-%m-%d')
    url = 'https://query.sse.com.cn/security/stock/queryCompanyBulletin.do?jsonCallBack=jsonpCallback15082809&isPagination=true&pageHelp.pageSize=25&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=1&productId={}&securityType=0101%2C120100%2C020100%2C020200%2C120200&reportType2=DQBG&reportType=YEARLY&beginDate={}&endDate={}&_={}'.format(
        code, beginDate, endDate, ts)

    payload = {}
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'ba17301551dcbaf9_gdp_session_id=ee252e6b-3eeb-4968-8ee6-64b5c77dd185; gdp_user_id=gioenc-3gb293c0%2C91d8%2C5b4c%2Ca47c%2C7057g2e38800; ba17301551dcbaf9_gdp_session_id_sent=ee252e6b-3eeb-4968-8ee6-64b5c77dd185; acw_sc__v2=67fe64fee2b2595f8ce7e282d5a59ba05256bfbc; JSESSIONID=8ED6E8153E9EEC7544EF81EFA26B89E6; ba17301551dcbaf9_gdp_sequence_ids={%22globalKey%22:158%2C%22VISIT%22:2%2C%22PAGE%22:16%2C%22VIEW_CLICK%22:90%2C%22VIEW_CHANGE%22:12%2C%22CUSTOM%22:42; JSESSIONID=AAC022612D78ED5875E2543833BA3DBA',
        'Host': 'query.sse.com.cn',
        'Referer': 'https://www.sse.com.cn/',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }

    response = requests.request('GET', url, headers=headers, data=payload)
    responseStr = response.text
    beg = responseStr.find('(')
    responseStr = responseStr[beg + 1:len(responseStr) - 1]
    jsonDict = json.loads(responseStr)
    data = jsonDict['pageHelp']['data']
    result = []
    for info in data:
        result.append({
            '标题': info['TITLE'],
            '下载路径': 'https://www.sse.com.cn' + info['URL']
        })
    return {'responseCode':'000000', 'responseMsg':'Success', 'data':result}


if __name__ == '__main__':
    mcp.run(transport="stdio")
