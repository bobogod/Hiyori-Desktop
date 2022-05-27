import itchat
import time
import threading
import requests
import json
import socket
from tkinter import *
from pyqrcode import QRCode
import os,io

class we_chat():
 def __init__(self,name,autotime,root,emerge,firsts): #传入各种参数，反馈各种参数
  self.root=root
  self.name=name
  self.autotime=autotime
  #itchat.auto_login(hotReload=True,enableCmdQR=True)
  
  for get_count in range(10):
        print('Getting uuid')
        uuid = itchat.get_QRuuid()
        while uuid is None: uuid = itchat.get_QRuuid();time.sleep(1)
        print('Getting QR Code')
        qrCode = QRCode('https://login.weixin.qq.com/l/' + uuid)
        qrStorage = io.BytesIO()
        if qrStorage:
         qrCode.png(os.getcwd()+'\\QR.png', scale=10)
         break
  

  
  qrtop=Toplevel(self.root,bg='black')
  qrtop.geometry('450x450+300+100')
  qrtop.overrideredirect(True)
  qrtop.title('qrtop')
  global t
  t=PhotoImage(file = 'QR.png')
  img=Label(qrtop,image=t)
  img.place(x=0,y=0)
  qrtop.update()
  print('finished')
  
  waitForConfirm = False
  while 1:
    status = itchat.check_login(uuid)
    if status == '200':
        break
    elif status == '201':
        if waitForConfirm:
            print('Please press confirm')
            waitForConfirm = True
    elif status == '408':
        print('Reloading QR Code')
        uuid = open_QR()
        waitForConfirm = False
  userInfo = itchat.web_init()
  itchat.show_mobile_login()
  #itchat.get_contract()
  #print('Login successfully as %s'%userInfo['NickName'])
  itchat.start_receiving()
  print('login successfully')
  qrtop.destroy()
  
  
  self.first,self.emergency={},{}
  self.stop=False
  for friend in itchat.get_friends():
    emerge[0].update({friend['RemarkName']:False})
    firsts[0].update({friend['RemarkName']:True})
  self.first=firsts[0]
  self.emergency=emerge[0]
    
 # tulinrobot接口联动
 def tulinRobotWechat(self,text,botapi):  
    apikeys=['e826608793bb4d68818c3539f8f0f6ef','491b3c02d3c84fea8fde57c84122176a','26ccc131e4664cf4bc98ae4e9d665edf','ebc4fab8b5d140b9b410e758ba4ca9da']
    url = "http://openapi.tuling123.com/openapi/api/v2"
    req = {
        "perception":
        {
            "inputText":
            {
                "text": text
            },
        },

        "userInfo": 
        {
            "apiKey": apikeys[botapi],
            "userId": "OnlyUs"
        }
    }
    req = json.dumps(req).encode('utf8')
    r = requests.post(url,data=req).json()
    code = r['intent']['code']
    if code == 10003:
        return "抱歉，我还没有能力播报新闻哦"
    elif code == 10015 or code == 10018:#dish
        return r['results'][1]['values']['text'] + "，链接：" + r['results'][0]['values']['url']
    else:#text
        if ('超过限制' in r['results'][0]['values']['text']) and ('请求' in r['results'][0]['values']['text']):
         return tulinRobotWechat(text,(botapi+1)%4)
        else:
         return r['results'][0]['values']['text']
    
 def wechatautorun(self,ret1,ret2,ret3,ret4,ret5,ret6,ret7,ret8):    #ret表示return，就是传回各种参数 
    @itchat.msg_register(itchat.content.TEXT)
    def print_content(msg):     #自动回复微信的核心部分
        if not self.stop:
         friend = itchat.search_friends(userName=msg['FromUserName'])
         remark = friend['RemarkName']
         if not self.emergency[remark]:
          if self.first[remark]:         
           self.first[remark]=False
           del ret5[0]
           ret5.append(self.first)
           return self.name+"不在，我是助手日和，如果有急事请输入\'有急事\'，您也可以和我聊天"
          else:
           if (('有急事' in msg['Text']) and (len(msg['Text'])<10)) or (('emergency' in msg['Text'].lower()) and (len(msg['Text'].split())<10)):
            #print('a',threading.active_count(),threading.currentThread())
            self.emergency[remark]=True
            del ret1[0]
            ret1.append(remark)
            del ret2[0]
            ret2.append(msg['FromUserName'])
            del ret3[0]
            ret3.append(self.emergency)
            del ret4[0]
            ret4.append(1)
            ret6.append(remark)
            return "[日和]好的，我现在就通知"+self.name
           else:
            return "[日和] "+ self.tulinRobotWechat(msg['Text'],3)  
         else:
          del ret7[0]
          ret7.append(ret6.index(remark))
          del ret8[0]
          ret8.append(msg['Text'])
          
    if self.autotime == 'forever':
        itchat.run(False,False)
        #print('b',threading.active_count(),threading.currentThread())
    else:
        a = threading.Timer(self.autotime,itchat.logout)
        #print('c',threading.active_count(),threading.currentThread())
        a.start()
        itchat.run(False,False)  
        #print('d',threading.active_count(),threading.currentThread())
  

