# -*- coding: utf-8 -*-

import itchat, time
import json
import random
from itchat.content import *
from data.city import city
from api.wxapi import *
import os
import re
import shutil

class ReplyData:
    __message = ''
    __username = ''

    def __init__(self,message,username):
        self.__message = message
        self.__username = username

    def find_reply_data(self):
        with open('./reply/reply_data.json','r',encoding = 'utf-8') as f:
            s = f.read()
            data = json.loads(s)
            for key in data:
                if self.__message.find(key) != -1:
                   return data[key]
            return self.__message

    def reply_data(self):
        if self.__message.find('天气详情') != -1: #天气关键字
            return self.find_weather_data()
        else: #命令模式
            data = self.find_reply_data()
            if data == self.__message:#robot API
                return find_robot(self.__message,self.__username)
            return data

    def find_weather_data(self):
        for key in city.keys():
            if self.__message.find(key) != -1:
                return query_weather(key)
        weatherData = query_weather('上海')#默认
        return weatherData

downloadDir = './download/'

@itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO])
def text_reply(msg):
    handler_receive_msg(msg)
    time.sleep(random.randint(4,10))
    if msg.type == TEXT:
        reply = ReplyData(msg.text,msg['FromUserName'])
        msg.user.send('%s' % (reply.reply_data()))
    elif msg.type == NOTE:
        pass
    elif msg.type == PICTURE or msg.type == RECORDING or msg.type == ATTACHMENT or msg.type == VIDEO:
        time.sleep(random.randint(15,30))
        msg.download(downloadDir + msg.fileName)
    else:
        msg.user.send('%s: %s' % ('我只会重复这句', msg.text))

#@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    time.sleep(random.randint(20,40))
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    return '@%s@%s' % (typeSymbol, msg.fileName)

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    print('添加好友',msg.user)
    #msg.user.verify()
    #msg.user.send('Nice to meet you!')

@itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING], isGroupChat=True)
def text_reply(msg):
    handler_group_receive_msg(msg)
    time.sleep(random.randint(6,12))
    if msg.isAt:
        reply = ReplyData(msg.text,msg.actualNickName)
        msg.user.send(u'@%s\u2005 %s' % (
            msg.actualNickName, reply.reply_data()))
    if msg.type == NOTE:#撤回通知
        pass

# 说明：可以撤回的有文本文字、语音、视频、图片、位置、名片、分享、附件
# {msg_id:(msg_from,msg_to,msg_time,msg_time_rec,msg_type,msg_content,msg_share_url)}
msg_dict = {}

# 文件存储临时目录
rev_tmp_dir = "./RevDir/"
if not os.path.exists(rev_tmp_dir): os.mkdir(rev_tmp_dir)

# 表情有一个问题 | 接受信息和接受note的msg_id不一致 巧合解决方案
face_bug = None


# 将接收到的消息存放在字典中，当接收到新消息时对字典中超时的消息进行清理 | 不接受不具有撤回功能的信息
# [TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO, FRIENDS, NOTE]
#@itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO])
def handler_receive_msg(msg):
    global face_bug
    # 获取的是本地时间戳并格式化本地时间戳 e: 2017-04-21 21:30:08
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 消息ID
    msg_id = msg['MsgId']
    # 消息时间
    msg_time = msg['CreateTime']
    # 消息发送人昵称 | 这里也可以使用RemarkName备注　但是自己或者没有备注的人为None
    msg_from = (itchat.search_friends(userName=msg['FromUserName']))["NickName"]
    # 消息内容
    msg_content = None
    # 分享的链接
    msg_share_url = None
    if msg['Type'] == 'Text' \
            or msg['Type'] == 'Friends':
        msg_content = msg['Text']
    elif msg['Type'] == 'Recording' \
            or msg['Type'] == 'Attachment' \
            or msg['Type'] == 'Video' \
            or msg['Type'] == 'Picture':
        msg_content = r"" + msg['FileName']
        # 保存文件
        msg['Text'](rev_tmp_dir + msg['FileName'])
    elif msg['Type'] == 'Card':
        msg_content = msg['RecommendInfo']['NickName'] + r" 的名片"
    elif msg['Type'] == 'Map':
        x, y, location = re.search(
            "<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
        if location is None:
            msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()
        else:
            msg_content = r"" + location
    elif msg['Type'] == 'Sharing':
        msg_content = msg['Text']
        msg_share_url = msg['Url']
    face_bug = msg_content
    # 更新字典
    msg_dict.update(
        {
            msg_id: {
                "msg_from": msg_from, "msg_time": msg_time, "msg_time_rec": msg_time_rec,
                "msg_type": msg["Type"],
                "msg_content": msg_content, "msg_share_url": msg_share_url
            }
        }
    )


# 收到note通知类消息，判断是不是撤回并进行相应操作
@itchat.msg_register(NOTE)
def send_msg_helper(msg):
    print('撤回消息处理...')
    global face_bug
    if re.search(r"\<\!\[CDATA\[.*撤回了一条消息\]\]\>", msg['Content']) is not None:
        # 获取消息的id
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        old_msg = msg_dict.get(old_msg_id, {})
        if len(old_msg_id) < 11:
            itchat.send_file(rev_tmp_dir + face_bug, toUserName='filehelper')
            os.remove(rev_tmp_dir + face_bug)
        else:
            msg_body = "告诉你一个秘密~" + "\n" \
                       + old_msg.get('msg_from') + " 撤回了 " + old_msg.get("msg_type") + " 消息" + "\n" \
                       + old_msg.get('msg_time_rec') + "\n" \
                       + "撤回了什么 ⇣" + "\n" \
                       + r"" + old_msg.get('msg_content')
            # 如果是分享存在链接
            if old_msg['msg_type'] == "Sharing": msg_body += "\n就是这个链接➣ " + old_msg.get('msg_share_url')

            # 将撤回消息发送到文件助手
            time.sleep(random.randint(6,12))
            itchat.send(msg_body, toUserName='filehelper')
            # 有文件的话也要将文件发送回去
            if old_msg["msg_type"] == "Picture" \
                    or old_msg["msg_type"] == "Recording" \
                    or old_msg["msg_type"] == "Video" \
                    or old_msg["msg_type"] == "Attachment":
                file = '@fil@%s' % (rev_tmp_dir + old_msg['msg_content'])
                itchat.send(msg=file, toUserName='filehelper')
                os.remove(rev_tmp_dir + old_msg['msg_content'])
            # 删除字典旧消息
            msg_dict.pop(old_msg_id)

#group chat
msg_group_dict = {}
# 文件存储临时目录
rev_group_tmp_dir = "./RevDir/Group/"

if not os.path.exists(rev_group_tmp_dir): os.mkdir(rev_group_tmp_dir)

def handler_group_receive_msg(msg):
    global face_bug
    # 获取的是本地时间戳并格式化本地时间戳 e: 2017-04-21 21:30:08
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 消息ID
    msg_id = msg['MsgId']
    # 消息时间
    msg_time = msg['CreateTime']
    # 消息发送人昵称 | 这里也可以使用RemarkName备注　但是自己或者没有备注的人为None
    msg_from = msg.actualNickName
    # 消息内容
    msg_content = None
    # 分享的链接
    msg_share_url = None
    if msg['Type'] == 'Text' \
            or msg['Type'] == 'Friends':
        msg_content = msg['Text']
    elif msg['Type'] == 'Recording' \
            or msg['Type'] == 'Attachment' \
            or msg['Type'] == 'Video' \
            or msg['Type'] == 'Picture':
        msg_content = r"" + msg['FileName']
        # 保存文件
        msg['Text'](rev_tmp_dir + msg['FileName'])
    elif msg['Type'] == 'Card':
        msg_content = msg['RecommendInfo']['NickName'] + r" 的名片"
    elif msg['Type'] == 'Map':
        x, y, location = re.search(
            "<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
        if location is None:
            msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()
        else:
            msg_content = r"" + location
    elif msg['Type'] == 'Sharing':
        msg_content = msg['Text']
        msg_share_url = msg['Url']
    face_bug = msg_content
    # 更新字典
    msg_group_dict.update(
        {
            msg_id: {
                "msg_from": msg_from, "msg_time": msg_time, "msg_time_rec": msg_time_rec,
                "msg_type": msg["Type"],
                "msg_content": msg_content, "msg_share_url": msg_share_url
            }
        }
    )

@itchat.msg_register(NOTE,isGroupChat=True)
def send_group_msg_helper(msg):
    print('群聊撤回消息处理...')
    global face_bug
    if re.search(r"\<\!\[CDATA\[.*撤回了一条消息\]\]\>", msg['Content']) is not None:
        # 获取消息的id
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        old_msg = msg_group_dict.get(old_msg_id, {})
        if len(old_msg_id) < 11:
            itchat.send_file(rev_group_tmp_dir + face_bug, toUserName=msg['FromUserName'])
            os.remove(rev_group_tmp_dir + face_bug)
        else:
            msg_body = "告诉你一个秘密~" + "\n" \
                       + old_msg.get('msg_from') + " 撤回了 " + old_msg.get("msg_type") + " 消息" + "\n" \
                       + old_msg.get('msg_time_rec') + "\n" \
                       + "撤回了什么 ⇣" + "\n" \
                       + r"" + old_msg.get('msg_content')
            # 如果是分享存在链接
            if old_msg['msg_type'] == "Sharing": msg_body += "\n就是这个链接➣ " + old_msg.get('msg_share_url')

            # 将撤回消息发送到文件助手
            time.sleep(random.randint(6,12))
            itchat.send(msg_body, toUserName=msg['FromUserName'])
            # 有文件的话也要将文件发送回去
            if old_msg["msg_type"] == "Picture" \
                    or old_msg["msg_type"] == "Recording":
                    #or old_msg["msg_type"] == "Video" \
                    #or old_msg["msg_type"] == "Attachment"
                file = '@fil@%s' % (rev_group_tmp_dir + old_msg['msg_content'])
                time.sleep(random.randint(6,12))
                itchat.send(msg=file, toUserName=msg['FromUserName'])
                os.remove(rev_group_tmp_dir + old_msg['msg_content'])
            # 删除字典旧消息
            msg_group_dict.pop(old_msg_id)

def lc():
    schedule_task('群消息自动回复任务')

itchat.auto_login(hotReload=True,loginCallback=lc)
itchat.run()
