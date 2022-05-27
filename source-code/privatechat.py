import itchat
import time
from tkinter import *
import requests
import json
import socket
        
        
class privateChat():
    def __init__(self,root,friendRemark,friendKey,name,emergency,firsts,index): #添加窗口和传入参数
        self.name=name
        self.index=index
        self.root = Toplevel(root,bg='Black')
        self.root.title("与" + friendRemark + "的私聊")
        self.mainFrame = Frame(self.root,background='Black')
        self.mainFrame.grid(row=0)
        self.sendFrame = Frame(self.root,background='Black')
        self.sendFrame.grid(row=1)

        self.msgtext = StringVar()
        self.remark = friendRemark
        self.key = friendKey
        self.flag = 1

        #消息列表
        self.mainText = Text(self.mainFrame,width=70,height=40,relief=FLAT,bd=3,bg='#222222',highlightthickness = 2,
                              highlightcolor = 'LightGrey',highlightbackground = 'LightGrey')
        self.mainText.grid(row=0,column=0,columnspan=2,padx=20,pady=20)
        self.mainText.tag_configure('time',foreground='CadetBlue',font=('Calibri',12))
        self.mainText.tag_configure('msg',foreground='#EEEEEE',font=('微软雅黑',12))
        self.mainText.tag_configure('warn',foreground='Red',font=('微软雅黑',12))
        
        #消息编辑框
        self.sendText = Entry(self.sendFrame,width=35,textvariable=self.msgtext,relief=FLAT,
                              bg='#222222',fg='#EEEEEE',font=('微软雅黑',15),highlightthickness = 2,
                              highlightcolor = 'White',highlightbackground = 'LightGrey')
        self.sendText.grid(row=1,column=0,padx=18,pady=20)
        self.sendText.bind('<Return>',self.__msgSendEvent)
        self.sendButton = Canvas(self.sendFrame,width=66,height=40,bg='Black',bd=0, highlightthickness=0)
        global im
        im.append(PhotoImage(file = 'button.gif'))    
        self.sendButton.create_image(20,20,image=im[-1])
        self.sendButton.grid(row=1,column=1,padx=0,pady=10,sticky=W)
        #self.sendButton.place(x=200,y=200)
        self.sendButton.bind('<Button-1>',self.__msgSendEvent)
        
        
        
    def __privateChatSend(self):
        tmp = self.msgtext.get()
        #真实发送
        itchat.send_msg(msg=tmp,toUserName = self.key)
        #显示在列表中
        content = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+'\n'
        self.mainText.insert(END,content,'time')
        self.mainText.insert(END,'我：'+ tmp +'\n','msg')
        self.sendText.delete(0,END)

    def __msgSendEvent(self,event):
        self.__privateChatSend()     
    
    def addmessage(self,st,kw):  #添加对话
      try:
        self.mainText.insert(END, st,kw)
      except:
        self.mainText.insert(END,'无法识别，请用手机微信查看\n','msg')
        
im=[]