# -*- coding: UTF-8 -*-

import urllib.request
import ssl
import json

def find_robot(message):
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
        return '晕了晕了,我需要休息一下。'
    content = res['content']
    return content
