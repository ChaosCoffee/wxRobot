# -*- coding: utf-8 -*-
import requests
import threading
import time,datetime
import schedule
import itchat
import random
from . import wxapi

hour = 12
minute = 30
execFlag = True
names = ['Test','测试'] 
execTime = "08:30"

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        log = wxapi.logger
        log.info("开始线程：" + self.name)
        run()
        log.info("退出线程：" + self.name)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

def get_news():
    wxapi.logger.info("金山词霸一日一句:")
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    return content, note

def send_news():
    i = datetime.datetime.now()
    wxapi.logger.info("newsAPI- 当前时间是 %s" % i)
    try:
        contents = get_news()
        #多群组则循环调用发送接口
        send_single_chatroom_msg(names[1],'[每日一句又来啦~]\n%s\n%s' % (contents[0],contents[1]),'每日一句')
    except:
        wxapi.logger.error("当天[每日一句]任务执行失败...")

def schedule_weather():
    i = datetime.datetime.now()
    wxapi.logger.info("WeatherAPI- 当前时间是 %s" % i)
    try:
        contents = wxapi.query_weather('上海')
        send_single_chatroom_msg(names[1],contents,'天气预报')
    except:
        wxapi.logger.error("当天[天气预报]任务执行失败...")

def schedule_news():
    # 每86400秒（1天），发送1次
    schedule.every().day.at("21:57").do(send_news)
    t = Timer(30, send_news)
    t.start()

#暂不支持多个群发送
def send_chatrooms_msg(senders,context,taskName):
    sender = senders[1] 
    itchat.get_chatrooms(update = True)
    iRoom = itchat.search_chatrooms(name = sender)
    for room in iRoom:
        if room['NickName'] == sender:
            userName = room['UserName']
            break
    time.sleep(random.randint(5,12))
    itchat.send_msg(context, userName)
    wxapi.logger.info("定时任务[%s],发送时间：[%s], 发送到: [%s], 发送内容：[%s]" ,taskName,datetime.datetime.now(), sender ,context)

def send_single_chatroom_msg(sender,context,taskName):
    itchat.get_chatrooms(update = True)
    iRoom = itchat.search_chatrooms(name = sender)
    #wxapi.logger.info(iRoom)
    for room in iRoom:
        if room['NickName'] == sender:
            userName = room['UserName']
            break
    time.sleep(random.randint(5,12))
    itchat.send_msg(context, userName)
    wxapi.logger.info("定时任务[%s],发送时间：[%s], 发送到: [%s], 发送内容：[%s]" ,taskName,datetime.datetime.now(), sender ,context)

def run():
    schedule.every().day.at(execTime).do(send_news) #规定每天08：30执行job()函数
    schedule.every().day.at('20:30').do(schedule_weather)
    while True:
        schedule.run_pending()#确保schedule一直运行
        time.sleep(30)