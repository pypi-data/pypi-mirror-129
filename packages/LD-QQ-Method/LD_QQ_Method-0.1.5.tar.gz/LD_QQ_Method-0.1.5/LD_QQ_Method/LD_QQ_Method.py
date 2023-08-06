from email import message
import requests
from urllib import parse
import base64
from requests import api
import threading
import json
import os
import console
import random
import time
import datetime
import fnmatch

from requests.models import encode_multipart_formdata


apiUrl = 'http://localhost:10002/MyQQHTTPAPI?'
TTSUrl = ''
TianXingKey = ''
welcom = ''
addMp3Url = ''
addAMRUrl = ''
imageUrl = ''
originUrl = ''
ttsVoiceUrl = ''
RobotQQ = ''

messageType = {
    '1'     : '好友',
    '2'     : '群聊',
    '1000'  : '单向添加好友',
    '1001'  : '被请求添加好友',
    '2003'  : '被邀请加入群聊',
    '80004' : '机器人发出消息'
}
color = ['\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m', '\033[37m']
quitGroupList = []
systemMenu = '管理员菜单：\n\\线程数目（检测当前线程，测试压力）\n\\检测管理（逐一检测群聊管理，退出非管理群聊）\n\\更新歌单（添加MP3格式文件后执行更新歌单）\n\\更新图片（添加图片后执行，图片名称即为匹配的关键字，格式为*jpg）\n\\自定义好友欢迎消息-\n\\自定义群聊欢迎消息-\n\\自定义群聊退出消息-\n\n含有-即为带参指令，-后填写参数\n例如：\\自定义好友欢迎消息-你好，我是天依'

# 机器人基础属性
class myRobot():
    def __init__(self, myApiUrl, myTTSUrl, myTianXingKey, mymyQQurl, myRobotQQ):
        global apiUrl
        global TTSUrl
        global TianXingKey
        global addMp3Url
        global addAMRUrl
        global imageUrl
        global originUrl
        global ttsVoiceUrl
        global RobotQQ
        apiUrl = myApiUrl
        TTSUrl = myTTSUrl
        TianXingKey = myTianXingKey
        addMp3Url = mymyQQurl + 'Voice/Music/MP3/'
        addAMRUrl = mymyQQurl + 'Voice/Music/AMR/'
        originUrl = mymyQQurl + 'Voice/Origin/'
        imageUrl = mymyQQurl + 'Image/'
        ttsVoiceUrl = mymyQQurl + 'Voice/'
        RobotQQ = myRobotQQ

# 初始化音频
def originAudio(fileName, auidoMessage):
    TTSDosynth = requests.get(TTSUrl + 'text=' + auidoMessage).json()
    code64 = TTSDosynth['data']
    code = base64.b64decode(code64)
    route = originUrl + fileName + '.mp3'
    tts = open(route, 'wb')
    tts.write(code)
    tts.close()
    routeMp3 = originUrl + fileName + '.mp3'
    routeAmr = originUrl + fileName + '.amr'
    AMRData = {
            'function'  : 'Api_Mp3ToAmr',
            'token'     : '666',
            'params'    : {
                'c1'        : routeMp3,
                'c2'        : routeAmr
            } 
        }
    requests.post(apiUrl, json=AMRData)
    os.remove(routeMp3)
    return

# 创建消息线程
class myThread(threading.Thread):
    def __init__(self, myname, my_raw_rev_data):
        threading.Thread.__init__(self)
        # self.myThread.name = myThread.name
        self.name = myname
        self.raw_rev_data_original = my_raw_rev_data
        self.raw_rev_data = my_raw_rev_data
        self.recRobot = ''
        self.recType = -1
        self.recID = ''
        self.recFromQQ = ''
        self.recMsg = ''
        self.image = ''
        self.colorFront = random.randint(31, 37)
        self.colorBack = random.randint(41, 47)
        while True:
            if (self.colorFront + 10) == self.colorBack:
                self.colorBack = random.randint(41, 47)
            else:
                break
    def run(self):
        msg = self.name + "：开始线程" 
        print (self.wordColor(msg))
        # 解析 raw_rev_data 文件
        raw_rev_data = json.loads(self.raw_rev_data)
        self.recRobot = raw_rev_data['MQ_robot']
        self.recType = raw_rev_data['MQ_type']
        self.recID = raw_rev_data['MQ_fromID']
        self.recFromQQ = raw_rev_data['MQ_fromQQ']
        self.recMsgData = raw_rev_data['MQ_msgData']
        self.recMsg = parse.unquote(raw_rev_data['MQ_msg'])
        # print(raw_rev_data)
        # 触发条件后根据实际情况处理调用情况
        if self.recType == 1 or (self.recType == 2 and not (self.recFromQQ == self.recRobot)):
            apiSendMsg(self)
        elif self.recType == 1000 or self.recType == 1001:
            agreeFriendEvent(self)
        elif self.recType == 2003:
            respondAddGroup(self)
        msg = self.name + "：退出线程" 
        print (self.wordColor(msg))
    # 文字颜色
    def wordColor(self, recMsg):
        recMsg = '\033['+ str(self.colorFront) + ';' + str(self.colorBack) + 'm' + recMsg + '\033[0m'
        return recMsg

# 创建时间线程
class timeThread(threading.Thread):
    def __init__(self, myRobotQQ, myisWhile):
        threading.Thread.__init__(self)
        global quitGroupList
        quitGroupList.clear()
        self.robotQQ = myRobotQQ
        self.robotGroup = ''
        self.isWhile = myisWhile
    def run(self):
        if self.isWhile:
            now_time = datetime.datetime.now()
            next_time = now_time + datetime.timedelta(days=+1)
            next_time = datetime.datetime.strptime(str(now_time.date().year)+"-"+str(now_time.date().month)+"-"+str(next_time.date().day)+" 00:00:00", "%Y-%m-%d %H:%M:%S")
            print(next_time)
            timer_start_time = (next_time - now_time).total_seconds()
            print(timer_start_time)
            time.sleep(timer_start_time)
            while self.isWhile:
                groupList(self)
        else:
            groupList(self)

# api消息回应
def apiSendMsg(myThread):
    try:
        myThread.recMsg = strQ2B(myThread.recMsg)
        fromQQName = getFriendsRemark(myThread)
        if myThread.recFromQQ == '3194775246' and myThread.recMsg[0] == '\\':
            systemSetting(myThread)
        elif myThread.recType == 1:
            msg = myThread.name + '：[' + messageType[str(myThread.recType)] + '] ' + fromQQName + '(' + myThread.recID + ')：' + myThread.recMsg
            print(myThread.wordColor(msg))
            if myThread.recMsg == '歌单':
                Music_showMenu(myThread)
            elif myThread.recMsg[0] == '唱':
                Music_singMusic(myThread)
            elif Image_find(myThread, myThread.recMsg):
                Image_send(myThread)
            else:
                prepareVoice(myThread)
                sendVoice_friend(myThread)
        elif myThread.recType == 2 and judgeAt(myThread.recMsg):
            groupName = getGroupName(myThread)
            msg = myThread.name + '：[' + messageType[str(myThread.recType)] + '] [' + groupName + ']' + fromQQName + '(' + myThread.recID + ')：' + myThread.recMsg
            print(myThread.wordColor(msg))
            myThread.recMsg = deleteAt(myThread.recMsg)
            print(myThread.recMsg)
            if myThread.recMsg == '歌单':
                Music_showMenu(myThread)
            elif myThread.recMsg[0] == '唱':
                Music_singMusic(myThread)
            elif Image_find(myThread, myThread.recMsg):
                Image_send(myThread)
            else:
                prepareVoice(myThread)
                sendVoice_group(myThread)
    except Exception as e:
        msg = 'error:', e
        print(myThread.wordColor(msg))

# 系统设置
def systemSetting(myThread):
    msgLen = len(myThread.recMsg)
    myThread.recMsg = myThread.recMsg[1:msgLen]
    if myThread.recMsg == '菜单':
        sendMsg_friend(myThread, myThread.recFromQQ, systemMenu)
    elif myThread.recMsg == '线程数目':
        sendMsg = '当前线程：' + str(len(threading.enumerate()))
        sendMsg_friend(myThread, myThread.recFromQQ, sendMsg)
    elif myThread.recMsg == '检测管理':
        global quitGroupList
        timeThread_temp = timeThread(RobotQQ, False)
        timeThread_temp.start()
        timeThread_temp.join()
        sendMsg = '已退出群聊：\n'
        for i in quitGroupList:
            sendMsg = sendMsg + str(i) + '\n'
        sendMsg_friend(myThread, myThread.recFromQQ, sendMsg)
    elif myThread.recMsg == '更新歌单':
        Music_Mp3toAMRMain(myThread)
    elif myThread.recMsg == '更新图片':
        Image_Main(myThread)
    elif myThread.recMsg[0 : 10] == '自定义好友欢迎消息-':
        custom_welcomFriend(myThread)
    elif myThread.recMsg[0 : 10] == '自定义群聊欢迎消息-':
        custom_addGroup(myThread)
    elif myThread.recMsg[0 : 10] == '自定义群聊退出消息-':
        custom_quitGroup(myThread)
    
# 自定义欢迎消息（好友）
def custom_welcomFriend(myThread):
    sendMsg_friend(myThread, myThread.recFromQQ, '正在进行好友欢迎信息自定义')
    welcomMsgLen = len(myThread.recMsg)
    welcomMsg = myThread.recMsg[10 : welcomMsgLen]
    originAudio('welcom', welcomMsg)
    msg = '好友欢迎信息自定义成功\n当前为：\n' + welcomMsg
    sendMsg_friend(myThread, myThread.recFromQQ, msg)

# 自定义群聊欢迎信消息
def custom_addGroup(myThread):
    sendMsg_friend(myThread, myThread.recFromQQ, '正在进行群聊欢迎信息自定义')
    addGroupLen = len(myThread.recMsg)
    addGroupMsg = myThread.recMsg[10 : addGroupLen]
    originAudio('addGroup', addGroupMsg)
    addGroup = open(originUrl + 'addGroup.txt', 'w+')
    addGroup.write(addGroupMsg)
    addGroup.close()
    msg = '群聊欢迎信息自定义成功\n当前为：\n' + addGroupMsg
    sendMsg_friend(myThread, myThread.recFromQQ, msg)

# 自定义群聊退出信消息
def custom_quitGroup(myThread):
    sendMsg_friend(myThread, myThread.recFromQQ, '正在进行群聊退出信息自定义')
    quitGroupLen = len(myThread.recMsg)
    quitGroupMsg = myThread.recMsg[10 : quitGroupLen]
    originAudio('quitGroup', quitGroupMsg)
    quitGroup = open(originUrl + 'quitGroup.txt', 'w+')
    quitGroup.write(quitGroupMsg)
    quitGroup.close()
    msg = '群聊退出信息自定义成功\n当前为：\n' + quitGroupMsg
    sendMsg_friend(myThread, myThread.recFromQQ, msg)

# 发送消息
def sendMsg_friend(myThread, sendNum, sendMsg):
    sendMsgData = {
        'function'  : 'Api_SendMsg',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : 1,
            'c3'        : '',
            'c4'        : sendNum,
            'c5'        : sendMsg
        }
    }
    requests.post(apiUrl, json=sendMsgData)
    msg = myThread.name + '：向' + getFriendsRemark(myThread) + '(' + sendNum + ')发送' + sendMsg
    try:
        print(myThread.wordColor(msg))
    finally:
        pass
def sendMsg_Group(myThread, sendNum, sendMsg):
    sendMsgData = {
        'function'  : 'Api_SendMsg',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : 2,
            'c3'        : sendNum,
            'c4'        : '',
            'c5'        : sendMsg
        }
    }
    requests.post(apiUrl, json=sendMsgData)
    msg = myThread.name + '：向' + getFriendsRemark(myThread) + '(' + sendNum + ')发送：' + sendMsg
    print(myThread.wordColor(msg))
def sendMsg_Group_QQ(robotQQ, sendNum, sendMsg):
    sendMsgData = {
        'function'  : 'Api_SendMsg',
        'token'     : '666',
        'params'    : {
            'c1'        : robotQQ,
            'c2'        : 2,
            'c3'        : sendNum,
            'c4'        : '',
            'c5'        : sendMsg
        }
    }
    requests.post(apiUrl, json=sendMsgData)
def sendMsg_Long_Group(myThread, sendNum, sendMsg):
    sendMsgData = {
        'function'  : 'Api_SendLongMsg',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : 0,
            'c3'        : 2,
            'c4'        : sendNum,
            'c5'        : '',
            'c6'        : sendMsg,
            'c7'        : 0
        }
    }
    requests.post(apiUrl, json=sendMsgData)
    msg = myThread.name + '：向' + getFriendsRemark(myThread) + '(' + sendNum + ')发送' + sendMsg
    print(myThread.wordColor(msg))

# 字典类型数据None数据处理功能
def dict_clean(items):
    result = {}
    for key, value in items:
        if value is None:
            value = '没有找到'
        result[key] = value
    return result

# 全角 -> 半角转换功能
def strQ2B(ustring):
    ss = ''
    for s in ustring:
        restring = ''
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 12288:                # 全角空格直接转换
                inside_code = 32
            elif 65281 <= inside_code <= 65374:     # 全角字符（除空格）根据关系转化
                inside_code -= 65248
            restring += chr(inside_code)
        ss += restring
    return ss

# 使用 VOCALTTS 获取mp3
def getTTStoMP3(myThread, TTSQuest):
    TTSDosynth = requests.get(TTSUrl + 'text=' + TTSQuest).json()
    code64 = TTSDosynth['data']
    code = base64.b64decode(code64)
    route = ttsVoiceUrl + myThread.name + '.mp3'
    tts = open(route, 'wb')
    tts.write(code)
    tts.close()
    msg = myThread.name + '：成功获取MP3'
    print(myThread.wordColor(msg))
    return

# 使用 天行机器人 获取回复内容
def getTianXing(myThread):
    TianXingData = {
            'key'       : TianXingKey,
            'question'  : '你好',
            'mode'      : 1
        }
    TianXingData['question'] = myThread.recMsg
    TianXingURL = 'http://api.tianapi.com/robot/index'
    TianXingPost = requests.post(TianXingURL, data=TianXingData).json()
    TianXingNewlist = TianXingPost['newslist']
    TianXingReply = TianXingNewlist[0]
    msg = myThread.name + '：AI(' + myThread.recRobot + ')：' + TianXingReply['reply']
    print(myThread.wordColor(msg))
    return TianXingReply['reply']

# Mp3 转 Amr
def getAmr(myThread):
    routeMp3 = ttsVoiceUrl + myThread.name + '.mp3'
    routeAmr = ttsVoiceUrl + myThread.name + '.amr'
    AMRData = {
            'function'  : 'Api_Mp3ToAmr',
            'token'     : '666',
            'params'    : {
                'c1'        : routeMp3,
                'c2'        : routeAmr
            }   
        }
    requests.post(apiUrl, json=AMRData)
    msg = myThread.name + '：成功获取AMR'
    print(myThread.wordColor(msg))
    os.remove(routeMp3)
    return

# 好友发送语音
def sendVoice_friend(myThread):
    routeAmr = ttsVoiceUrl + myThread.name + '.amr'
    SendVoiceData = {
        'function'  : 'Api_SendVoice',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : myThread.recID,
            'c3'        : routeAmr
        }
    }
    requests.post(apiUrl, json=SendVoiceData)
    os.remove(routeAmr)
    msg = myThread.name + '：向' + myThread.recID + '发送音频'
    print(myThread.wordColor(msg))

# 上传语音
def upLoadVoice(myThread):
    routeAmr = ttsVoiceUrl + myThread.name + '.amr'
    upLoadVoiceData = {
        'function'  : 'Api_UpLoadVoice',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : routeAmr
        }
    }
    GUIDData = requests.post(apiUrl, json=upLoadVoiceData).json()
    GUIDret = GUIDData['data']
    msg = myThread.name + '：语音上传成功'
    print(myThread.wordColor(msg))
    return GUIDret['ret']

# 群聊发送语音
def sendVoice_group(myThread):
    routeAmr = ttsVoiceUrl + myThread.name + '.amr'
    GUID = upLoadVoice(myThread)
    sendVoiceData = {
        'function'  : 'Api_SendMsg',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : 2,
            'c3'        : myThread.recID,
            'c4'        : '',
            'c5'        : GUID
        }
    }
    requests.post(apiUrl, json=sendVoiceData)
    os.remove(routeAmr)
    msg = myThread.name + '：向' + myThread.recID + '发送音频'
    print(myThread.wordColor(msg))

# 音频准备
def prepareVoice(myThread):
    # 使用 天行机器人 获取回复内容
    reply = getTianXing(myThread)
    # 使用 VOCALTTS 获取mp3
    getTTStoMP3(myThread, reply)
    # Api_Mp3ToAmr
    getAmr(myThread)
    return

# 判断 @
def judgeAt(recMsg):
    RobotQQLen = len(RobotQQ)
    if recMsg[0 : (RobotQQLen + 3)] == '[@'+ RobotQQ +']':
        return True
    else:
        return False

# 除去 @
def deleteAt(recMsg):
    RobotQQLen = len(RobotQQ)
    msgLen = len(recMsg)
    recMsg = recMsg[(RobotQQLen + 4) : msgLen]
    return recMsg

# 同意好友添加
def agreeFriendEvent(myThread):
    HandleFriendEventData = {
        'function'  : 'Api_HandleFriendEvent',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : myThread.recFromQQ,
            'c3'        : 10,
            'c4'        : ''    
        }
    }
    requests.post(apiUrl, json=HandleFriendEventData)
    welcomSend(myThread)

# 好友添加发送语音
def welcomSend(myThread):
    routeAmr = originUrl + 'welcom.amr'
    SendVoiceData = {
        'function'  : 'Api_SendVoice',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : myThread.recFromQQ,
            'c3'        : routeAmr
        }
    }
    requests.post(apiUrl, json=SendVoiceData)
    msg = myThread.name + '：向' + myThread.recFromQQ + '发送欢迎音频'
    print(myThread.wordColor(msg))

# 获取好友备注
def getFriendsRemark(myThread):
    GetFriendsRemarkData = {
        'function'  : 'Api_GetFriendsRemark',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : myThread.recFromQQ
        }
    }
    recFromQQName = requests.post(apiUrl, json=GetFriendsRemarkData).json()
    fromQQNameData = recFromQQName['data']
    fromQQName = fromQQNameData['ret']
    return fromQQName

# 取用户名
def getNick(myThread):
    getNickData = {
        'function'  : 'Api_GetNick',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : myThread.recFromQQ
        }
    }
    recPersonName = requests.post(apiUrl, json=getNickData).json()
    personNameData = recPersonName['data']
    personName = personNameData['ret']
    return personName

# 获取群名称
def getGroupName(myThread):
    getGroupNameData = {
        'function'  : 'Api_GetGroupNameEx',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : myThread.recID
        }
    }
    recGroupName = requests.post(apiUrl, json=getGroupNameData).json()
    groupNameData = recGroupName['data']
    groupName = groupNameData['ret']
    return groupName

# 回应邀请入群
def respondAddGroup(myThread):
    groupName = getGroupName(myThread)
    presonName = getNick(myThread)
    msg = myThread.name + '：[' + messageType[str(myThread.recType)] + ']'+ presonName + '(' + myThread.recFromQQ + ') 邀请你加入群聊：' + groupName + '(' + myThread.recID + ')'
    print(myThread.wordColor(msg))
    agreeGroupEvent(myThread)

# 同意加入群聊
def agreeGroupEvent(myThread):
    HandleGroupEventData = {
        'function'  : 'Api_HandleGroupEvent',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : myThread.recMsgData,
            'c3'        : 10,
            'c4'        : '',
            'c5'        : 0
        }
    }
    requests.post(apiUrl, json=HandleGroupEventData)
    groupName = getGroupName(myThread)
    msg = myThread.name + '：加入群聊[' + groupName + '(' + myThread.recID + ')]'
    routeAmr = originUrl + 'addGroup.amr'
    upLoadVoiceData = {
        'function'  : 'Api_UpLoadVoice',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : routeAmr
        }
    }
    GUIDData = requests.post(apiUrl, json=upLoadVoiceData).json()
    GUIDret = GUIDData['data']
    msg = myThread.name + '：语音上传成功'
    print(myThread.wordColor(msg))
    GUID = GUIDret['ret']
    sendVoiceData = {
        'function'  : 'Api_SendMsg',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : 2,
            'c3'        : myThread.recID,
            'c4'        : '',
            'c5'        : GUID
        }
    }
    requests.post(apiUrl, json=sendVoiceData)
    addGroupFile = open(originUrl + 'addGroup.txt', 'r+')
    addGroup = addGroupFile.read()
    sendMsg_Group(myThread, myThread.recID, addGroup)
    msg = myThread.name + '：向' + myThread.recID + '发送音频'
    print(myThread.wordColor(msg))

# 获取群列表
def groupList(timeThread):
    getGroupListData = {
        'function'  : 'Api_GetGroupList',
        'token'     : '666',
        'params'    : {
            'c1'        : timeThread.robotQQ,
        }
    }
    recGroupList = requests.post(apiUrl, json=getGroupListData).json()
    recGroupListData = recGroupList['data']
    recGroupListRet = recGroupListData['ret']
    recGroupListData = recGroupListRet['data']
    recGroupListGroup = recGroupListData['group']
    for i in recGroupListGroup:
        qq = i['groupcode']
        timeThread.robotGroup = qq
        if not(judgeAdmin(timeThread)):
            quitGroupEvent(timeThread)
       
# 判断是否是管理
def judgeAdmin(timeThread):
    getAdminListData = {
        'function'  : 'Api_GetAdminList',
        'token'     : '666',
        'params'    : {
            'c1'        : timeThread.robotQQ,
            'c2'        : timeThread.robotGroup
        }
    }
    recAdminList = requests.post(apiUrl, json=getAdminListData).json()
    recAdminListData = recAdminList['data']
    recAdminListRet = recAdminListData['ret']
    recAdminListRet = recAdminListRet.strip()
    groupAdmin = []
    groupAdminID = ''
    for j in recAdminListRet:
        if not(j == '\n'):
            groupAdminID = groupAdminID + j
        else:
            groupAdmin.append(groupAdminID.strip())
            if not(groupAdminID == ''):
                groupAdminID = ''
    groupAdmin.append(groupAdminID.strip())
    for j in groupAdmin:
        if timeThread.robotQQ == j:
            return True
    return False

# 退群
def quitGroupEvent(timeThread):
    global quitGroupList
    quitGroupList.append(timeThread.robotGroup)
    routeAmr = originUrl + 'quitGroup.amr'
    upLoadVoiceData = {
        'function'  : 'Api_UpLoadVoice',
        'token'     : '666',
        'params'    : {
            'c1'        : timeThread.robotQQ,
            'c2'        : routeAmr
        }
    }
    GUIDData = requests.post(apiUrl, json=upLoadVoiceData).json()
    GUIDret = GUIDData['data']
    GUID = GUIDret['ret']
    sendVoiceData = {
        'function'  : 'Api_SendMsg',
        'token'     : '666',
        'params'    : {
            'c1'        : timeThread.robotQQ,
            'c2'        : 2,
            'c3'        : timeThread.robotGroup,
            'c4'        : '',
            'c5'        : GUID
        }
    }
    requests.post(apiUrl, json=sendVoiceData)
    quitGroupFile = open(originUrl + 'quitGroup.txt', 'r+')
    quitGroup = quitGroupFile.read()
    quitGroupFile.close()
    sendMsg_Group_QQ(timeThread.robotQQ, timeThread.robotGroup, quitGroup)
    quitGroupData = {
        'function'  : 'Api_QuitGroup',
        'token'     : '666',
        'params'    : {
            'c1'        : timeThread.robotQQ,
            'c2'        : timeThread.robotGroup
        }
    }
    requests.post(apiUrl, json=quitGroupData).json()
    print('timeThread：退出' + str(timeThread.robotGroup))

# 获取Music文件名（删去扩展名）
def Music_getMusicName(musicName):
    musicNameLen = len(musicName)
    musicName = musicName[0 : (musicNameLen - 4)]
    return musicName

# 添加 Mp3音乐文件到amr
def Music_Mp3toAMR(musicName):
    routeMp3 = addMp3Url + musicName + '.mp3'
    routeAmr = addAMRUrl + musicName + '.amr'
    AMRData = {
            'function'  : 'Api_Mp3ToAmr',
            'token'     : '666',
            'params'    : {
                'c1'        : routeMp3,
                'c2'        : routeAmr
            }   
        }
    requests.post(apiUrl, json=AMRData)
    os.remove(routeMp3)
    return

# 添加Music.txt文件
def Music_addMusicTXT(musicNameList):
    musicTXT = open(addAMRUrl + 'Music.txt', 'w+')
    allName = ''
    for i in musicNameList:
        allName = allName + i + '\n'
    musicTXT.write(allName)
    musicTXT.close()

# 读取Music.txt文件
def Music_readMusicTXT():
    musicTXT = open(addAMRUrl + 'Music.txt', 'r+')
    allName = musicTXT.readlines()
    addName = []
    for i in allName:
        i = i.strip('\n')
        addName.append(i)
    musicTXT.close()
    return addName

# 读取文件夹下所有mp3/amr格式文件名(list)
def Music_readMusicName(path, format):
    name = [name for name in os.listdir(path) if fnmatch.fnmatch(name, format)]
    return name    

# Mp3 转 Amr 主程序
def Music_Mp3toAMRMain(myThread):
    musicNameListmp3 = Music_readMusicName(addMp3Url, '*mp3')
    sendMsg = '音频转化已完成：\n'
    for i in musicNameListmp3:
        if not Music_JudgeMusic(i):
            i = Music_getMusicName(i)
            Music_Mp3toAMR(i)
            sendMsg = sendMsg + i +'\n'
            msg = i + '-已添加完成'
            sendMsg_friend(myThread, myThread.recFromQQ, msg)
    musicNameListAMR = Music_readMusicName(addAMRUrl, '*amr')
    musicNameList = []
    for i in musicNameListAMR:
        i = Music_getMusicName(i)
        musicNameList.append(i)
    Music_addMusicTXT(musicNameList)
    sendMsg_friend(myThread, myThread.recFromQQ, sendMsg)
    msg = myThread.name + '：音频转化完成'
    print(myThread.wordColor(msg))

# 展示歌单
def Music_showMenu(myThread):
    musicList = Music_readMusicTXT()
    menuMsg = '歌单如下：\n'
    for i in musicList:
        menuMsg = menuMsg + '《' + i + '》'
    menuMsg = menuMsg + '\n如果想要天依唱歌，请发送唱+歌名，如：唱亲爱的'
    print(menuMsg)
    if myThread.recType == 1:
        sendMsg_friend(myThread, myThread.recFromQQ, menuMsg)
    elif myThread.recType == 2:
        sendMsg_Group(myThread, myThread.recID, menuMsg)

# 判断曲目是否在歌单中
def Music_JudgeMusic(musicName):
    musicList = Music_readMusicTXT()
    for i in musicList:
        if musicName == i:
            return True
    return False

# 向群聊发送歌曲
def Music_snedMusic_group(myThread, musicName):
    routeAmr = addAMRUrl + musicName + '.amr'
    upLoadVoiceData = {
        'function'  : 'Api_UpLoadVoice',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : routeAmr
        }
    }
    GUIDData = requests.post(apiUrl, json=upLoadVoiceData).json()
    GUIDret = GUIDData['data']
    sendVoiceData = {
        'function'  : 'Api_SendMsg',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : 2,
            'c3'        : myThread.recID,
            'c4'        : '',
            'c5'        : GUIDret['ret']
        }
    }
    requests.post(apiUrl, json=sendVoiceData) 

# 向好友发送歌曲
def Music_snedMusic_friend(myThread, musicName):
    routeAmr = addAMRUrl+ musicName + '.amr'
    SendVoiceData = {
        'function'  : 'Api_SendVoice',
        'token'     : '666',
        'params'    : {
            'c1'        : myThread.recRobot,
            'c2'        : myThread.recID,
            'c3'        : routeAmr
        }
    }
    requests.post(apiUrl, json=SendVoiceData)

# 发送歌曲
def Music_singMusic(myThread):
    musicName = myThread.recMsg
    lenName = len(musicName)
    musicName = musicName[1 : lenName]
    if Music_JudgeMusic(musicName):
        if myThread.recType == 1:
            Music_snedMusic_friend(myThread, musicName)
        else:
            Music_snedMusic_group(myThread, musicName)
    else:
        msg = '天依暂时还没有收录该曲目，小伙伴可以联系管理员收录该曲目哦！'
        if myThread.recType == 1:
            sendMsg_friend(myThread, myThread.recFromQQ, msg)
        else:
            sendMsg_Group(myThread, myThread.recID, msg)

# 发送图片
def Image_send(myThread):
    imageRoute = imageUrl + myThread.image + '.jpg'
    upLoadPicData = {
        'function'  : 'Api_UpLoadPic',
        'token'     : '666',
        'params'    : {
            'c1'    : myThread.recRobot,
            'c2'    : myThread.recType,
            'c3'    : '3194775246',
            'c4'    : imageRoute
        }
    }
    imageGUIDrec = requests.post(apiUrl, json=upLoadPicData).json()
    imageGUIDData = imageGUIDrec['data']
    imageGUID = imageGUIDData['ret']
    if myThread.recType == 1:
        sendMsg_friend(myThread, myThread.recFromQQ, imageGUID)
    elif myThread.recType == 2:
        sendMsg_Group(myThread, myThread.recID, imageGUID)

# 添加Image.txt文件
def Image_addImageTXT(imageNameList):
    imageTXT = open(imageUrl + 'Image.txt', 'w+')
    allName = ''
    for i in imageNameList:
        allName = allName + i + '\n'
    imageTXT.write(allName)
    imageTXT.close()

# 读取Image.txt文件
def Image_readImageTXT():
    imageTXT = open(imageUrl + 'Image.txt', 'r+')
    allName = imageTXT.readlines()
    addName = []
    for i in allName:
        i = i.strip('\n')
        addName.append(i)
    imageTXT.close()
    return addName

# 读取文件夹下所有*jpg格式文件名(list)
def Image_readImageName(path, format):
    name = [name for name in os.listdir(path) if fnmatch.fnmatch(name, format)]
    return name  

# 判断关键词，返回关键词
def Image_find(myThread, msg):
    imageList = Image_readImageTXT()
    for i in imageList:
        if i in msg:
            myThread.image = i
            return True
    return False

# 更新Image
def Image_Main(myThread):
    sendMsg_friend(myThread, myThread.recFromQQ, '开始更新Image关键词')
    imageName = Image_readImageName(imageUrl, '*jpg')
    print(imageName)
    imageNameList = []
    # 借用Music除去Image扩展名
    for i in imageName:
        i = Music_getMusicName(i)
        imageNameList.append(i)
    Image_addImageTXT(imageNameList)
    msg = 'Image关键词更新完毕\n当下列表：\n'
    for i in imageNameList:
        msg = msg + i + '\n'
    sendMsg_friend(myThread, myThread.recFromQQ, msg)