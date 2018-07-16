# -*- coding: utf-8 -*-

import urllib.request
import time
import ssl
import json
import threading

L = threading.Lock() # 引入锁
 
class Weather:
     def query_weather(self,query):
        ssl._create_default_https_context = ssl._create_unverified_context
        url = r"https://www.sojson.com/open/api/weather/json.shtml?city=%s" % (urllib.parse.quote(query))#一个提供区域天气预报的url
        L.acquire()    # 加锁
        time.sleep(3)    #此处等待3秒主要是对应网页提示，三秒内只能访问一次
        page = urllib.request.urlopen(url)
        L.release()    # 释放锁
        # # ssl._create_default_https_context=ssl._create_unverified_context
        html = page.read().decode("utf-8")

        '''
            json.dumps()和json.loads()是json格式处理函数（可以这么理解，json是字符串）
            (1)json.dumps()函数是将一个Python数据类型列表进行json格式的编码（可以这么理解，json.dumps()函数是将字典转化为字符串）
            (2)json.loads()函数是将json格式数据转换为字典（可以这么理解，json.loads()函数是将字符串转化为字典）
        '''

        res = json.loads(html)
        a = json.dumps(res, ensure_ascii=False, indent=4)          #将读取到的内容格式化，这样就可以看到有缩进、换行的内容
        # print(a)
        fp = open(r"./data/weather.txt", "w",encoding='UTF-8') #将读取内容保存到文件
        fp.write(a) #写入数据
        fp.close() #关闭文件

        res = json.loads(a) #将json转化为dict
        # print(res)

        '''
        通过查看抓到的代码，发现dict中嵌套了dict，所以需要把对应的dict取出来
        同样，forecast中，在list里嵌套了dict，需要仔细查看并设置中间变量
        '''
        now = res['data']
        forcast = now['forecast']
        today = forcast[0]
        tomorrow = forcast[1]      #注意看res文件内容，forecast其实是一个list，其元素才是dict
        tomorrowAfter = forcast[2]
        
        weatherData = "%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s" % (
                "========今日天气========",
                "日期：           " + today['date'],
                "城市：           " + res['city'],
                "最高温度：     " + today['high'],
                "最低温度：     " + today['low'],
                "天气状况：     " + today['type'],
                "湿度：           " + now['shidu'],
                "PM2.5：        " + str(now['pm25']),
                "空气质量：     " + now['quality'],
                "温馨提示：     " + today['notice'],
                "\n",
                "========明日预报========",
                "日期：           " + tomorrow['date'],
                "最高温度：     " + tomorrow['high'],
                "最低温度：     " + tomorrow['low'],
                "天气状况：     " + tomorrow['type'],
                "温馨提示：     " + tomorrow['notice'],
                "\n",
                "=========后日预报========",
                "日期：           " + tomorrowAfter['date'],
                "最高温度：     " + tomorrowAfter['high'],
                "最低温度：     " + tomorrowAfter['low'],
                "天气状况：     " + tomorrowAfter['type'],
                "温馨提示：     " + tomorrowAfter['notice']) 
        return weatherData
        
        '''
        print("\n\n")
        print("===============今日天气===============")
        print("日期：       ",res['date'])
        print("城市：       ",res['city'])
        print("温度：       ",today['wendu'])
        print("湿度：       ",today['shidu'])
        print("PM2.5：     ",today['pm25'])
        print("空气质量：    ",today['quality'])

        print("\n\n")
        print("===============昨日天气===============")
        print("日期：          ",yesterday['date'])
        print("城市：          ",res['city'])
        print("最高温度：       ",yesterday['high'])
        print("最低温度：       ",yesterday['low'])
        print("天气状况：       ",yesterday['type'])
        # print("PM2.5：     ",today['pm25'])
        # print("空气质量：    ",today['quality'])

        print("\n\n")
        print("===============明日预报===============")
        print("日期：          ",tomorrow['date'])
        print("城市：          ",res['city'])
        print("最高温度：       ",tomorrow['high'])
        print("最低温度：       ",tomorrow['low'])
        print("天气状况：       ",tomorrow['type'])
        print("温馨提醒：       ",tomorrow['notice'])
        # print("PM2.5：     ",today['pm25'])
        # print("空气质量：    ",today['quality'])


        '''