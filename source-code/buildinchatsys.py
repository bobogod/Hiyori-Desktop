import itchat
import time
import datetime
import requests
import json
import socket
import wechatauto
from tkinter import *
from num2chinese import *

# 获取本地地址，但是会出bug，弃用了
def ip2geo():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    apiurl = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" %ip
    content = requests.get(apiurl).text
    data = json.loads(content)['data']
    code = json.loads(content)['code']
    if code == 0:
        if data['city']=="内网IP":
            return 1
        return data
    else:
        return 0

class ChatSys():
    def __init__(self,time,root,name):
        self.botapi=3
        self.w=None
        self.root=root
        self.time=time
        self.emergency=[{}]
        self.remark=[None]
        self.index=[None]
        self.first=[0]
        self.firsts=[{}]
        self.wins=[]
        self.currentuser=[None]
        self.currentmsg=[None]
        self.name=name
    

    def printOut(self,text):  #输出到待语音合成的txt
        with open(r"textfromgirl.txt","w") as f:
            for each in text:
                flag,s,eacht=False,'',''
                for i in each:
                 if i in '0123456789':
                  flag=True
                  s+=i
                 elif flag:
                  flag=False
                  if not i in ['年']:
                   s=rankis(int(s))
                  eacht+=s+i
                  s=''
                 else:
                  eacht+=i
                if flag:
                  if eacht!='' and eacht[-1]!=':':
                   s=rankis(int(s))
                  eacht+=s
                each=eacht
                each.replace(u'\xa0', u'')
                each.replace(u'\u3000',u'')
                each.replace(u'\n',u'')
                each.replace(u'\r',u'')
                for i in each:
                 if i==' ':
                  each=each[:each.find(i)]+','+each[each.find(i)+1:]
                 if i=='.':
                  each=each[:each.find(i)]+'点'+each[each.find(i)+1:]
                #print('each=',each)
                print(each,file = f)
        f.close
        
    def tulinRobotBuildIn(self,text,during_study):  #桌面的智能聊天
        apikeys=['e826608793bb4d68818c3539f8f0f6ef','26ccc131e4664cf4bc98ae4e9d665edf','491b3c02d3c84fea8fde57c84122176a','ebc4fab8b5d140b9b410e758ba4ca9da']  #因为没钱所以多申请了几个api
        #loc = ip2geo()
        loc={'city':'北京','region':'北京'}
        dat = ['','']
        if loc == 1:
            dat[0]="北京"
            dat[1]="北京"
        elif loc == 0:
            pass
        else:
            dat[0]=loc['city']
            dat[1]=loc['region']
        
        url = "http://openapi.tuling123.com/openapi/api/v2"
        req = {
            "perception":
            {
                "inputText":
                {
                    "text": text
                },

                "selfInfo":
                {
                    "location":
                    {
                        "city": dat[0],
                        "province": dat[1]
                    }
                }
            },

            "userInfo": 
            {
                "apiKey": apikeys[self.botapi],
                "userId": "OnlyUs"
            }
        }
        req = json.dumps(req).encode('utf8')
        r = requests.post(url,data=req).json()
        
        content = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        insertstr=[]
        voicestr=[]
        code = r['intent']['code']
        if code == 10003:#news
            insertstr.append('日和：'+ '找到今天的新闻啦！')
            voicestr.append('找到今天的新闻啦！')
            for i in range(len(r['results'][1]['values']['news'])):
                insertstr.append(r['results'][1]['values']['news'][i]['name'])
                voicestr.append(r['results'][1]['values']['news'][i]['name']+'。')
                insertstr.append(r['results'][1]['values']['news'][i]['detailurl'])
            insertstr.append('新闻播报完毕，来源：新浪新闻。')
            voicestr.append('新闻播报完毕，来源：新浪新闻。')
        else:
            tmp = r['results'][0]['values']['text']
            if tmp == '请问需要更换哪一款壁纸呢？':  #这里都是一些特判
                insertstr.append('日和：'+ tmp )
                voicestr.append( tmp )
            elif tmp == '请自由地调节音量吧~':
                insertstr.append('日和：'+ tmp )
                voicestr.append( tmp )
            elif tmp == '好的！但还是先设置一下吧。':
                if during_study: tmp='已经在学习模式了，不能偷懒哦！'  
                insertstr.append('日和：'+ tmp)
                voicestr.append( tmp )          
            elif tmp == '下面开启微信自动回复，请扫码登录Web版微信。':
                insertstr.append('日和：'+ tmp )
                voicestr.append( tmp )
                self.wechatAuto()
            elif tmp == '您真的要退出吗？':
                insertstr.append('日和：'+ tmp )
                voicestr.append( tmp )
                itchat.logout()
            else:
                insertstr.append('日和：'+ tmp )
                voicestr.append( tmp )
        if ('请求' in tmp) and ('超过限制' in tmp):
         self.botapi=(self.botapi+1)%4
         return self.tulinRobotBuildIn(text,root)
        else:
         self.printOut(voicestr)
         return insertstr
        
    def wechatAuto(self):  #设置微信自动回复的
        self.top = Toplevel(self.root)
        self.top.resizable(0,0)
        self.top.geometry('360x140')
        self.top.title('开启微信自动回复')
        
        self.label = Label(self.top,text='请选择微信自动回复的时长：')
        self.label.grid(row=0,column=0,columnspan=3,sticky=W,padx=10,pady=10)
        global v
        v = IntVar()
        self.choice1 = Radiobutton(self.top,text='定时结束',variable=v,value=1,command=self.__enable)
        self.choice1.grid(row=1,column=0,sticky=W,padx=10)
        self.choice2 = Radiobutton(self.top,text='程序关闭自动结束',variable=v,value=0,command=self.__disable)
        self.choice2.grid(row=2,column=0,sticky=W,padx=10)

        self.entryH = Entry(self.top,width=7)
        self.entryH.grid(row=1,column=1,sticky=W)
        self.entryHL = Label(self.top,text='h').grid(row=1,column=2,sticky=W,padx=5)
        self.entryM = Entry(self.top,width=7)
        self.entryM.grid(row=1,column=3,sticky=W)
        self.entryML = Label(self.top,text='min').grid(row=1,column=4,sticky=W,padx=5)

        self.confirm = Button(self.top,text='确定',width=8,command=self.__timeConfirm).grid(row=3,column=2,columnspan=2,padx=5,sticky=S)
        self.cancel = Button(self.top,text='取消',width=8,command=self.__cancel).grid(row=3,column=4,columnspan=2,padx=5,sticky=S)

    def __enable(self):
        self.entryH['state']='normal'
        self.entryM['state']='normal'
        
    def __disable(self):
        self.entryH['state']='disabled'
        self.entryM['state']='disabled'

    def __timeConfirm(self): #内部调用wechatauto
        mytime = 0
        if v.get() == 1:
            h = self.entryH.get().strip()
            m = self.entryM.get().strip()
            if h == '':h='0'
            if m == '':m='0'
            try:
                mytime = float(h)*3600 + float(m)*60
            except ValueError:
                messagebox.showerror("错误","请输入正数")
                return
        elif v.get() == 0:
            mytime = 'forever'
        self.top.destroy()
        self.w=wechatauto.we_chat(self.name,mytime,self.root,self.emergency,self.firsts)
        self.w.wechatautorun(self.remark,self.index,self.emergency,self.first,self.firsts,self.wins,self.currentuser,self.currentmsg)
     
    '''def changeemergency(self,user,em):
     self.emergency[user]=em
     if self.w!=None:
      self.w.change_emergency(self.emergency)'''
    
    def __cancel(self):
        self.top.destroy()

    def timeconfirm(self): #外部调用wechatauto
     if itchat.check_login()!='200':
      self.w=wechatauto.we_chat(self.name,self.time,self.root,self.emergency,self.firsts)
      self.w.wechatautorun(self.remark,self.index,self.emergency,self.first,self.firsts,self.wins,self.currentuser,self.currentmsg)
     else:
      self.start()
      
    def start(self): #继续托管
     if self.w!=None:
      self.w.stop=False
    
    def stop(self):  #暂停托管
     if self.w!=None:
      self.w.stop=True