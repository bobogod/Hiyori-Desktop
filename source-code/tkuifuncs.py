import tkinter as tk
import pyglet
import os,ctypes,threading
from tkinter import filedialog,messagebox
import json,socket,requests
  
class tkuifuncs:
 def __init__(self): pass
 
 def overrideiconify():
  top.overrideredirect(False)
  top.iconify()
 
 def changebg(args): #切换壁纸
  win=args[1]
  #print('success in calling changebg')
  name=filedialog.askopenfilename(filetypes=[('JPG','*.jpg'),('PNG','*.png'),('BMP','*.bmp'),('All Files','*')])
  if name!='':
   bgname=name[name.rfind('/')+1:]
   if not 'resources/wallpapers/' in name:
    #print('cd \"'+name[:name.rfind('/')]+'\" & '+name[:name.find(':')+1]+' & copy \"'+bgname+'\" \"'+os.getcwd()+'\\resources\\wallpapers\"')
    os.system('cd \"'+name[:name.rfind('/')]+'\" & '+name[:name.find(':')+1]+' & copy \"'+bgname+'\" \"'+os.getcwd()+'\\resources\\wallpapers\"')
   pyglet.resource.path=['resources/wallpapers']
   pyglet.resource.reindex()
   bg=pyglet.sprite.Sprite(pyglet.resource.image(bgname))
   bg.update(scale_x=win.width/bg.width,scale_y=win.height/bg.height)
   pyglet.resource.path=['resources']
   pyglet.resource.reindex()
   #print('changebg finished')
   args[0]=[bg,bgname]
  
 def sndvol(args):  #调音量
  def ossndvol():
   os.system('sndvol')
  threading.Thread(target=ossndvol,args=()).start()
  
 def study(args):  #调学习模式
  root,win,icons=args[0],args[1],args[5]
  topstudy=tk.Toplevel(root)
  topstudy.title('study settings')
  topstudy.geometry('520x360+'+str(win.width//2-260)+'+'+str(win.height//2-200))
  topstudy.resizable(0,0)
  
  l1=tk.Label(topstudy,text='学习模式时间段:')
  l1.place(x=20,y=18)
  h1=tk.Spinbox(topstudy,from_=0,to=23,width=2)
  maohao1=tk.Label(topstudy,text=':')
  m1=tk.Spinbox(topstudy,from_=0,to=59,width=2)
  gang=tk.Label(topstudy,text='——')
  h2=tk.Spinbox(topstudy,from_=0,to=23,width=2)
  maohao2=tk.Label(topstudy,text=':')
  m2=tk.Spinbox(topstudy,from_=0,to=59,width=2)
  h1.place(x=120,y=20)
  maohao1.place(x=155,y=18)
  m1.place(x=170,y=20)
  gang.place(x=202,y=18)
  h2.place(x=240,y=20)
  maohao2.place(x=275,y=18)
  m2.place(x=290,y=20)
  
  scroll=tk.Scrollbar(topstudy)
  scroll.place(x=493,y=20,height=148)
  timelist=tk.Listbox(topstudy,yscrollcommand=scroll.set,height=8)
  timelist.place(x=350,y=20)
  scroll.config(command=timelist.yview)
  
  times=list(args[2])
  for time in times: timelist.insert(tk.END,str(time[0]//60)+':'+str(time[0]%60)+' —— '+str(time[1]//60)+':'+str(time[1]%60))
  
  def addtime(): 
   nonlocal times
   t1=int(h1.get())*60+int(m1.get())
   t2=int(h2.get())*60+int(m2.get())
   if t1<t2:
    flag=True
    timest=list(times)
    for each in timest:
     if not ((t1>each[1]) or (t2<each[0])):
      if flag:
       flag=False
       old=timest[timest.index(each)]
       old[0]=min(t1,each[0])
       old[1]=max(t2,each[1])
      else:
       old[0]=min(each[0],old[0])
       old[1]=max(each[1],old[1])
       timest.remove(each)
    if flag:
     timest.append([t1,t2]) 
    for i in range(len(timest)):
     t=i
     for j in range(i+1,len(timest)):
      if timest[j][0]<timest[t][0]:
       t=j
     timest[t],timest[i]=timest[i],timest[t]
    times=timest 
    timelist.delete(0,tk.END)
    for time in times:
      timelist.insert(tk.END,str(time[0]//60)+':'+str(time[0]%60)+' —— '+str(time[1]//60)+':'+str(time[1]%60))
   else:
    tk.messagebox.showerror('错误','不是有效的时间段')
     
  def deltime():
   nonlocal times
   time=int(timelist.curselection()[0])
   del times[time]
   timelist.delete(time)
   
  def savedesk():
   #print(icons)
   f=open(os.getcwd()+'\\studysave.dat','w')
   for each in icons: 
    f.write(each.path+'\n')
    f.write(each.iconame+'\n')
   f.close()
   
  
  addtimebutton=tk.Button(topstudy,text=' 添加时间段 ',command=addtime)
  addtimebutton.place(x=120,y=50)
  deltimebutton=tk.Button(topstudy,text=' 删除时间段 ',command=deltime)
  deltimebutton.place(x=220,y=50)
  
  autostudyv,autoreplyv=tk.StringVar(),tk.StringVar()
  autostudyv.set(args[3][0])
  autoreplyv.set(args[4][0])
  savedeskbutton=tk.Button(topstudy,text='    保存当前桌面为学习桌面    ',command=savedesk) 
  savedeskbutton.place(x=120,y=100)
  autostudybutton=tk.Checkbutton(topstudy,text='根据时间段自动进入学习模式',variable=autostudyv)
  autostudybutton.place(x=120,y=130)
  autoreplybutton=tk.Checkbutton(topstudy,text='进入学习模式自动托管微信',variable=autoreplyv)
  autoreplybutton.place(x=120,y=155)
  
  
  def addweb():
   webt=webin.get()
   webs=list(weblist.get(0,tk.END))
   if not webt in webs:
    webs.append(webt)
   weblist.delete(0,tk.END)
   for web in webs:
     weblist.insert(tk.END,web)
  
  def delweb():
   webindex=int(weblist.curselection()[0])
   weblist.delete(webindex)
  
  scroll2=tk.Scrollbar(topstudy)
  scroll2.place(x=493,y=190,height=148)
  l2=tk.Label(topstudy,text='学习时禁用网页:')
  l2.place(x=20,y=190)
  webin=tk.Entry(topstudy,width=28)
  webin.place(x=120,y=190)
  weblist=tk.Listbox(topstudy,yscrollcommand=scroll2.set,height=8)
  weblist.place(x=350,y=190)
  scroll2.config(command=weblist.yview)
  addwebbutton=tk.Button(topstudy,text=' 添加 网页 ',command=addweb)
  delwebbutton=tk.Button(topstudy,text=' 删除 网页 ',command=delweb)
  addwebbutton.place(x=120,y=235)
  delwebbutton.place(x=220,y=235)
  f=open('C:\\Windows\\System32\\drivers\\etc\\hosts1','r')
  listf=f.readlines()
  for each in listf: weblist.insert(tk.END,each[10:len(each)-1])
  
  
 
  def savesettings():
   t=len(args[2])
   for i in range(t):
    del args[2][0]
   for time in times:
    args[2].append(time)
   
   
   f=open('C:\\Windows\\System32\\drivers\\etc\\hosts1','w')
   webs=list(weblist.get(0,tk.END))
   for web in webs: f.write('127.0.0.1 '+web+'\n')
   f.close()
   
   f=open('C:\\Windows\\System32\\drivers\\etc\\hosts','w')
   for web in webs: f.write('127.0.0.1 '+web+'\n')
   f.close()
   
   f=open(os.getcwd()+'\\studytimesave.dat','w')
   for time in times:
    f.write(str(time[0])+' '+str(time[1])+'\n')
   f.close()
   
   args[3][0]=autostudyv.get()
   args[4][0]=autoreplyv.get()
   
   quit()
   
  
  def quit():
   topstudy.destroy()
  
  
  savesettingbutton=tk.Button(topstudy,text=' 保存 设置 ',command=savesettings)
  savesettingbutton.place(x=120,y=280)
  quitbutton=tk.Button(topstudy,text='    取 消    ',command=quit)
  quitbutton.place(x=220,y=280)
 
 def console(args):  #调出控制台
  whnd = ctypes.windll.kernel32.GetConsoleWindow()
  if whnd != 0:  ctypes.windll.user32.ShowWindow(whnd, 1)
  
 def wifi(args):   #连接wifi，不过只能连接连过的，如果连接没连过的不会报错，但没有网
  root,win=args[0],args[1]
  topwifi=tk.Toplevel(root)
  topwifi.title('wifi settings')
  topwifi.geometry('300x100+'+str(win.width//2-150)+'+'+str(win.height//2-50))
  topwifi.resizable(0,0)
  result = os.popen('netsh wlan show networks').read()
  networknames=[]
  for line in result.splitlines():
   if 'SSID' in line:
    a=line[9:]
    networknames.append(a)

  selected=tk.StringVar()
  selected.set(networknames[0])
  wlans=tk.OptionMenu(topwifi,selected,*networknames)
  linked=os.popen('netsh wlan show interfaces').read()

  x=tk.StringVar()
  if 'SSID' in linked:
   for line in linked.splitlines():
    if 'SSID' in line:
     x.set('WIFI: '+line[28:]+' connected')
     break
  else:
   x.set('WIFI not connected')
   
  now=tk.Label(topwifi,textvariable=x)
  text=tk.Label(topwifi,text='WIFI: ')
  now.place(x=10,y=20)
  text.place(x=10,y=55)
  wlans.place(x=50,y=50)
  
  def connect():
   t=selected.get()
   ret=os.popen('netsh wlan connect name='+t+' ssid='+t).read()
   if ('success' in ret) or ('成功' in ret): 
    tk.messagebox.showinfo('连接成功','WIFI: '+t+' connected')
    x.set('WIFI:  '+t+' connected')
   
  connectbutton=tk.Button(topwifi,text=' 连 接 ',command=connect)
  connectbutton.place(x=240,y=50)
  
 def other(args):  #其他
  #print('success in calling other')
  root,win=args[0],args[1]
  topother=tk.Toplevel(root)
  topother.title('others')
  topother.geometry('520x540+'+str(win.width//2-260)+'+'+str(win.height//2-270))
  topother.resizable(0,0)
  
  def savename():
   args[2][0]=getname.get()
   url = "http://openapi.tuling123.com/openapi/api/v2"
   req = {
            "perception":
            {
                "inputText":
                {
                    "text": '我叫'+args[2][0]
                },

                "selfInfo":
                {
                    "location":
                    {
                        "city": '北京',
                        "province": '北京'
                    }
                }
            },

            "userInfo": 
            {
                "apiKey": 'ebc4fab8b5d140b9b410e758ba4ca9da',
                "userId": "OnlyUs"
            }
        }
   req = json.dumps(req).encode('utf8')
   r = requests.post(url,data=req).json()
   tk.messagebox.showinfo('保存成功','恭喜你，'+args[2][0]+'，保存成功')
  
  getnamelabel=tk.Label(topother,text='看板娘该怎么称呼你：')
  getname=tk.Entry(topother,width=30)
  getname.insert(tk.END,args[2][0])
  getnamesave=tk.Button(topother,text='保存称呼',command=savename)
  getnamelabel.place(x=20,y=20)
  getname.place(x=170,y=20)
  getnamesave.place(x=410,y=16)

  aboutdoc=("""
    本桌面系统作者：波、玻璃
    联系方式： 波微信:qfdz01  玻璃微信:丝竹乱  
    --------------------------------
    看板娘部分采用live2d技术
    智能聊天采用图灵机器人的api
    语音合成采用讯飞开放平台的api
    由于资金问题
    智能聊天2019-7-5前每日上限约5000次交互
    7-5后每日上限降为约300次，需要您的支持！
    语音合成每日上限约500次
    --------------------------------
    目前本软件仅支持windows系统
    在向桌面添加程序时
    需要找到能打开的exe文件或对应的lnk文件
    其中，浏览器和office系列软件
    建议在网上先搜索相关知识
    找到其安装目录运行相关exe
    --------------------------------
    如果遇到BUG或有建议，请联系作者
    如果需要python源码，也请联系作者
    如果觉得这个软件很好，请扫码支持
  """)
  abouttext=tk.Text(topother,font=('微软雅黑',11),width=55,height=23,bd=0)
  abouttext.insert(tk.INSERT,aboutdoc)  
  abouttext.place(x=10,y=60)
  global pic1,pic2
  pic1=tk.PhotoImage(file='resources/boli.png')
  pic1label=tk.Label(topother,image=pic1,bd=0) 
  pic1label.place(x=305,y=420)
  pic2=tk.PhotoImage(file='resources/bobo.png')
  pic2label=tk.Label(topother,image=pic2,bd=0) 
  pic2label.place(x=405,y=420)
  #print('get a test here')