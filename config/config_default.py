# -*- coding: utf-8 -*-

'''
Default configurations.
'''

configs = {
    'debug': True,
    'robotName': '二蛋',
    'times': {
        'friend': {
            'start': 4,
            'end': 8  
        },
        'group': {
            'start': 5,
            'end': 10
        },
        'pushMessage': {
            'start': 6,
            'end': 12  
        },
        'download': {
             'start': 15,
             'end': 30
        },
        'withdraw': {
             'start': 10,
             'end': 20
        }
    },
    'chatrooms': ['Test','测试'],
    'schedule': {
        'news': {
            'selected': 1,
            'isExec': True,
            'execTime': '08:30'
        },    
        'weather': {
            'selected': 1,
            'isExec': True,
            'execTime': '20:30'
        }    
    },
    'keyword': {
        'K0001': '天气详情',#查询天气
        'K0002': '上海',#默认查询天气城市
        'K0003': '晕了晕了,我需要休息一下。',#请求出错默认回复
        'K0004': '我累了，不想回答，只想睡觉觉~' #图灵次数用完回复
    },
    'path': {
        'reply': './reply/reply_data.json',
        'downloadDir': './download/',
        'revDir': './RevDir/',
        'revGroupDir': './RevDir/Group/'
    },
    'withdrawGroupMessage': {
        'sender': 'FromUserName'#FromUserName 发送者，filehelper 文件助手      
    },
    'robot': {
        'userRobot': 'tuling', 
        'tuling': {
            'apiUrl': 'http://www.tuling123.com/openapi/api',
            'apiKey': 'awadafaswad213154456sasdad'
        },
        'qingke': {
            'url': ''
        }
    }
}