# -*- coding: utf-8 -*-
import requests
import threading
import time,datetime
import schedule
import itchat
import random
import logging
from config.config import configs
from .import wxapi

log = logging.getLogger('news')
_chatrooms = configs.chatrooms
_newsExecTime = configs.schedule.news.execTime
_weatherExecTime = configs.schedule.weather.execTime
_start = configs.times.pushMessage.start
_end = configs.times.pushMessage.end

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        log.info("开始线程：" + self.name)
        run()
        log.info("退出线程：" + self.name)

def print_time(threadName, delay, counter):
    exitFlag = False
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

def get_news():
    log.info("金山词霸一日一句:")
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    return content, note

def send_news():
    i = datetime.datetime.now()
    log.info("newsAPI- 当前时间是 %s" % i)
    try:
        contents = get_news()
        #多群组则循环调用发送接口
        send_single_chatroom_msg(_chatrooms[configs.schedule.news.selected],'[每日一句又来啦~]\n%s\n%s' % (contents[0],contents[1]),'每日一句')
    except:
        log.error("当天[每日一句]任务执行失败...")

def schedule_weather():
    i = datetime.datetime.now()
    log.info("WeatherAPI- 当前时间是 %s" % i)
    try:
        contents = wxapi.query_weather(configs.keyword.K0002)
        send_single_chatroom_msg(_chatrooms[configs.schedule.weather.selected],contents,'天气预报')
    except:
        log.error("当天[天气预报]任务执行失败...")

def schedule_news():
    # 每86400秒（1天），发送1次
    schedule.every().day.at(_newsExecTime).do(send_news)
    t = Timer(30, send_news)
    t.start()

#Expired 暂不支持多个群发送
def send_chatrooms_msg(senders,context,taskName):
    log.info("定时任务开始发送[%s],发送时间：[%s], 发送到: [%s], 发送内容：[%s]" ,taskName,datetime.datetime.now(), sender ,context)
    itchat.get_chatrooms(update = True)
    iRoom = itchat.search_chatrooms(name = sender)
    for room in iRoom:
        if room['NickName'] == sender:
            userName = room['UserName']
            break
    time.sleep(random.randint(_start,_end))
    itchat.send_msg(context, userName)
    log.info("定时任务完成[%s],发送时间：[%s], 发送到: [%s], 发送内容：[%s]" ,taskName,datetime.datetime.now(), sender ,context)

def send_single_chatroom_msg(sender,context,taskName):
    log.info("定时任务开始发送[%s],发送时间：[%s], 发送到: [%s], 发送内容：[%s]" ,taskName,datetime.datetime.now(), sender ,context)
    itchat.get_chatrooms(update = True)
    iRoom = itchat.search_chatrooms(name = sender)
    for room in iRoom:
        if room['NickName'] == sender:
            userName = room['UserName']
            break
    time.sleep(random.randint(_start,_end))
    itchat.send_msg(context, userName)
    log.info("定时任务完成[%s],发送时间：[%s], 发送到: [%s], 发送内容：[%s]" ,taskName,datetime.datetime.now(), sender ,context)

def run():
    if configs.schedule.news.isExec: 
        schedule.every().day.at(_newsExecTime).do(send_news) #规定每天08：30执行job()函数
        log.info('[%s] 任务初始化完成,启动时间: [%s], 任务时间: [%s][%s]','每日一句',datetime.datetime.now(),'每日',_newsExecTime)
    if configs.schedule.weather.isExec:
        schedule.every().day.at(_weatherExecTime).do(schedule_weather)
        log.info('[%s] 任务初始化完成,启动时间: [%s], 任务时间: [%s][%s]','天气预报',datetime.datetime.now(), '每日',_weatherExecTime)
    while True:
        schedule.run_pending()#确保schedule一直运行
        time.sleep(30)