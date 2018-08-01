# -*- coding: UTF-8 -*-

import urllib.request
import ssl
import json
import requests
from config.config import configs

_resContent = configs.keyword.K0003
_apiKey = configs.robot.tuling.apiKey

def find_robot(message):
    return message

def qingke_robot():
    ssl._create_default_https_context = ssl._create_unverified_context
    url = r"http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s" % (
        urllib.parse.quote(message))  # 一个提供区域天气预报的url
    page = urllib.request.urlopen(url)
    html = page.read().decode("utf-8")
    res = json.loads(html)
    # 将读取到的内容格式化，这样就可以看到有缩进、换行的内容
    a = json.dumps(res, ensure_ascii=False, indent=4)
    #print(a)
    code = res['result']
    if code != 0:
        return _resContent
    content = res['content']
    return content

def tuling_robot(message,userid):
    data = {
        'key'    : _apiKey,
        'info'   : message, 
        'userid' : userid
    }
    r = requests.post(configs.robot.tuling.apiUrl, data=data).json() #需要根据不同code返回
    msg = ''
    #print(r)
    if r['code'] == 100000: #文本
        msg = r.get('text')
    elif r['code'] == 200000: #链接类
        msg = '%s~\n查看链接: [%s]' % (r.get('text'),r.get('url'))
    elif r['code'] == 302000: #新闻类
        dictNews = r['list']
        msg = r.get('text') + '~'
        for i in range(6 if len(dictNews) > 6 else len(dictNews)):
            news = dictNews[i]
            msg = ('%s\n[%d]\n新闻标题: [%s]\n新闻来源: [%s]\n新闻图片: [%s]\n详情链接: [%s]') % (msg,i,news['article'],
                news['source'],'抱歉，暂未找到图片' if news['icon'] == "" else news['icon'],
                news['detailurl'])
    elif r['code'] == 308000: #菜谱类
        dictMenus = r['list']
        msg = r.get('text') + '~'
        for i in range(6 if len(dictMenus) > 6 else len(dictMenus)):
            menu = dictMenus[i]
            msg = ('%s\n[%d]\n菜名: [%s]\n查看美食：[%s]\n菜谱信息: [%s]\n详情链接: [%s]') % (msg,i,menu['name'],
                '抱歉，暂未找到图片' if menu['icon'] == "" else menu['icon'],
                menu['info'],menu['detailurl'])
    elif r['40004'] == 40004:# 当天请求次数已使用完
        msg = configs.keyword.K0004
    return msg or _resContent

if __name__ == "__main__":
    msg = tuling_robot('我想看新闻','wechat-robot')
    print(msg)