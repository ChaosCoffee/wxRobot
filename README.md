# wxRobot  

微信聊天机器人，支持群聊，个人，文件传输助手等聊天窗口  
<!-- TOC -->

- [wxRobot](#wxrobot)
    - [itchat](#itchat)
    - [emoji表情代码](#emoji表情代码)
    - [配置文件](#配置文件)
    - [扩展API](#扩展api)
        - [天气预报](#天气预报)
        - [智能机器人API](#智能机器人api)
            - [图灵机器人](#图灵机器人)
            - [青云客机器人](#青云客机器人)
        - [推送任务](#推送任务)
        - [消息撤回](#消息撤回)
        - [机器人开关](#机器人开关)

<!-- /TOC -->
## wxRobot文档
[wxRobot文档](https://github.com/ChaosCoffee/wxRobot)

## itchat
采用开源ItChat，使用Python调用微信接口，API文档如下
[itchat](http://itchat.readthedocs.io/zh/latest/)  

安装itchat:  
> pip install itchat  

##  emoji表情代码
[表情代码](http://www.wqchat.com/emoji.html)  

[表情复制](http://www.oicqzone.com/tool/emoji/)

## 配置文件 
见根目录下config文件目录下的config_default.py,支持被config_override.py覆盖配置
引用则使用 `configs`

## 扩展API
### 天气预报 

输入关键字`天气` ,`xxx天气` 获取不同地区城市的天气预报

+<img src="https://raw.githubusercontent.com/ChaosCoffee/wxRobot/master/docs/intro/image/weather.png" width=128 />
  

### 智能机器人API
#### 图灵机器人
[图灵机器人](http://www.tuling123.com/)

- 智能工具
  - 生活百科
  - 数字计算
  - 中英互译
  - 问答百科
  - 图片搜索(暂不支持)
- 休闲娱乐  
  - 笑话大全
  - 故事大全
  - 成语接龙
  - 新闻资讯
  - 星座运势
  - 脑筋急转弯
  - 歇后语
  - 绕口令
  - 顺口溜
  - 斗图(暂不支持)
- 生活服务
  - 天气查询
  - 菜谱大全
  - 快递查询
  - 列车查询
  - 日期查询
  - 附近酒店
  - 汽油报价
  - 股票查询
  - 城市邮编  
  
#### 青云客机器人
[青云客](http://www.qingyunke.com/)   
> 支持功能：天气、翻译、藏头诗、笑话、歌词、计算、域名信息/备案/收录查询、IP查询、手机号码归属、人工智能聊天。
  
**参数说明**  

|功能  | 示例  |   
|--------| -------- |   
|天气 | 天气深圳 |
|中英翻译  | 翻译i love you |
|歌词⑴ | 歌词后来 |
|歌词⑵  | 歌词后来-刘若英 |
|计算⑴  | 计算1+1*2/3-4 |
|计算⑵  | 1+1*2/3-4 |
|域名⑴  | 域名github.com |
|域名⑵  | github.com |
|ＩＰ⑴  | 归属127.0.0.1 |
|ＩＰ⑵  | 127.0.0.1 |
|手机⑴  | 归属13430108888 |
|手机⑵  | 13430108888 |
|笑话  | 笑话 |
|智能聊天  | 你好 |  

### 推送任务  
定时向个人或者群聊中推送天气预报，每日一句等消息

### 消息撤回
监听消息撤回通知

### 机器人开关  
自定义消息发送,可以对机器人是否自动回复进行控制












































