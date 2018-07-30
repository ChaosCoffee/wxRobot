#-*- coding:utf-8 -*-

import logging
from . import robot,weather,news
import time,functools
import urllib.error

logger = logging.getLogger() # logging对象
fh = logging.FileHandler("./log/wxapi-log.log") # 文件对象
sh = logging.StreamHandler() # 输出流对象
fm = logging.Formatter('%(asctime)s-%(filename)s[line%(lineno)d]-%(levelname)s- %(message)s') # 格式化对象
fh.setFormatter(fm) # 设置格式
sh.setFormatter(fm) # 设置格式
logger.addHandler(fh) # logger添加文件输出流
logger.addHandler(sh) # logger添加标准输出流（std out）
logger.setLevel(logging.INFO) # 设置从那个等级开始提示

def log(apiname):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            start = time.time()
            res = func(*args, **kw)
            end = time.time()
            logger.info('[%s] 返回结果: [%s], 请求信息: [%s], 执行耗时: [%s] s', apiname, res, str(args),end - start)
            #print('%s %s():' % (text, func.__name__))
            return res
        return wrapper
    return decorator

@log('RobotAPI')
def find_robot(message,userid):
    content = ''
    useRobot = 2
    try: 
        if useRobot == 1: 
            content = robot.qingke_robot(message).replace("{br}","\n").replace("菲菲","二蛋")
        elif useRobot == 2:
            content = robot.tuling_robot(message,userid)
        else:
            content = '晕了晕了,我需要休息一下。'
        #logger.info('[RobotAPI] 返回结果: [%s], 请求信息: [%s]', content, message)
    except urllib.error.HTTPError as err:
        logger.error('RobotAPI request error',err)
        content = '晕了晕了,我需要休息一下。'
    return content

@log('WeatherAPI')
def query_weather(message):
    content = ''
    try:
        content = weather.query_weather(message)
    #logger.info('[WeatherAPI] 返回结果: [%s], 请求信息: [%s]', content, message)
    except urllib.error.HTTPError as err:
        logger.error('WeatherAPI request error',err)
        content = '晕了晕了,我需要休息一下。'
    return content


@log('NewsAPI')
def schedule_task(message):
    logger.info("NewsAPI start running...")
    thread1 = news.myThread(1, "Thread-1", 1)
    thread1.start()
