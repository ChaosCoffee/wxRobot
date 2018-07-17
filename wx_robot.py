# -*- coding: utf-8 -*-

import itchat, time
import json
from itchat.content import *
from data.city import city
from api.wxapi import *

class ReplyData:
    __message = ''

    def __init__(self,message):
        self.__message = message

    def find_reply_data(self):
        with open('./reply/reply_data.json','r',encoding = 'utf-8') as f:
            s = f.read()
            data = json.loads(s)
            #print(data)
            for key in data:
                if self.__message.find(key) != -1:
                   return data[key]
            return self.__message

    def reply_data(self):
        if self.__message.find('天气') != -1: #天气关键字
            return self.find_weather_data()
        else: #命令模式
            data = self.find_reply_data()
            if data == self.__message:#robot API
                return find_robot(self.__message)
            return data

    def find_weather_data(self):
        for key in city.keys():
            if self.__message.find(key) != -1:
                return query_weather(key)
        weatherData = query_weather('上海')#默认
        return weatherData

            
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    if msg.type == TEXT:
        reply = ReplyData(msg.text)
        msg.user.send('%s' % (reply.reply_data()))
    else:
        msg.user.send('%s: %s' % ('我只会重复这句', msg.text))

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    return '@%s@%s' % (typeSymbol, msg.fileName)

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('Nice to meet you!')

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.isAt:
        reply = ReplyData(msg.text)
        msg.user.send(u'@%s\u2005 %s' % (
            msg.actualNickName, reply.reply_data()))
        
itchat.auto_login(hotReload=True)
itchat.run()