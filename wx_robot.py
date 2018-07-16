# -*- coding: utf-8 -*-

import itchat, time
import json
from itchat.content import *
from data.city import city
from api.weather import *

class ReplyData:
    def find_reply_data(self, str):
        with open('./reply/reply_data.json','r',encoding = 'utf-8') as f:
            s = f.read()
            data = json.loads(s)
            #print(data)
            for key in data:
                if str.find(key) != -1:
                   return data[key]
                   
            return data['default']
            
    def find_weather_data(self, str):
        weather = Weather()
        for key in city.keys():
            if str.find(key) != -1:
                weatherData = weather.query_weather(key)
                return weatherData
        weatherData = weather.query_weather('上海')
        return weatherData

            
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    if msg.type == TEXT:
        message = msg.text
        if message.find('天气') != -1:
            reply = ReplyData()
            msg.user.send(reply.find_weather_data(message))        
        else:
            msg.user.send('%s: %s' % ('我只会重复这句', msg.text))        
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
        print(msg.text)
        str = msg.text
        reply = ReplyData()
        data = reply.find_reply_data(str)
        msg.user.send(u'@%s\u2005 %s' % (
            msg.actualNickName, data))
        
itchat.auto_login(hotReload=True)
itchat.run()