#学习模式：指定时间内，无法退出、更改软件、设置网页、调节微信提醒模式(默认部分提醒)、设置壁纸
#自由模式：学习时间外，可以更改软件、设置网页、退出、调节微信提醒模式(默认全部提醒)、设置壁纸、设置微信自动回复
#两模式下都可以与看板娘互动
#紧急退出：学习模式下右键settingbutton输入密码退出学习模式

import os,sys,ctypes,gc,psutil,threading  #涉及系统和功能的一些包
import random,time,chardet
from win32.lib import win32con
from win32api import GetSystemMetrics
import win32api,win32con,win32process,win32gui
import itchat

import pyglet                             #涉及ui界面的一些包
from pyglet.window import mouse,key 
from tkinter import filedialog
import tkinter as tk

import tkuifuncs                          #自己写的py
import buildinchatsys
from MyButton import *
from icons_right import *
import window2iconame as w2i
import w32window
import privatechat
# 在工作目录中选择一个gif动画文件

from tkinter import filedialog,messagebox  #担心pyinstaller打包时出错，导入的包
import requests
import json
import socket
import datetime



class PowerClass(ctypes.Structure):#获取电源信息
    _fields_ = [('ACLineStatus', ctypes.c_byte),
            ('BatteryFlag', ctypes.c_byte),
            ('BatteryLifePercent', ctypes.c_byte),
            ('Reserved1',ctypes.c_byte),
            ('BatteryLifeTime',ctypes.c_ulong),
            ('BatteryFullLifeTime',ctypes.c_ulong)]
powerclass = PowerClass()

# -----------------------------------------------
def foo(hwnd,mouse):  #搜索获得目前所有打开的窗口的句柄和名称
 global title,hwnds
 #title=set()
 #title,hwnds=[],[]
 pdlist=['Program Manager','开始','管理员','tk','小火箭通用加速','看板娘学习桌面','ChatContactMenu']
 if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and (win32gui.IsWindowVisible(hwnd) or win32gui.IsIconic(hwnd)):
  t=win32gui.GetWindowText(hwnd)
  if t!='':
   flag=True  
   for each in pdlist:
    if each in t:
     flag=False
     break
   #if flag: title.append(t)
   if flag and t not in title: 
    title.append(t)
    if hwnd not in hwnds: hwnds.append(hwnd)
    
    
'''def fooclear(hwnd,mouse):       #关闭所有窗口用的
 if win32gui.IsWindow(hwnd): #and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
  t=win32gui.GetWindowText(hwnd)
  if t!='':      
   if 'Program Manager' not in t:
     if '开始' not in t:
      if '管理员' not in t:
       if 'main.py' not in t:
        try:
         win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        except:
         pass'''
   

   
       
def exe(path):  #运行main中管理的所有按钮的功能
   global win,icons,turnoffbutton,addbutton,settingbutton,minusbutton,during_minus,studybutton
   #print(path)
   if 'setting_bo_specialized' in path:
    settingbutton.change_scale(3.3-settingbutton.smallscale,1.8)
    turnoffbutton.visible=not turnoffbutton.visible
    addbutton.visible=not addbutton.visible
    minusbutton.visible=not minusbutton.visible
    systembutton.visible=not systembutton.visible
    if settingbutton.dx==0: settingbutton.on_press()
    settingbutton.dx,settingbutton.dy=4-settingbutton.dx,3-settingbutton.dy
    print(settingbutton.incollider)
    
   elif 'turnoff_bo_specialized' in path:
    win.exit_window()
    itchat.logout()
    save(icons,bg_bgname)
    os.system('cd C:/Windows & C: & start explorer.exe')
    sys.exit()
    
   elif 'add_bo_specialized' in path:
    t=addicons(win,icons)
    icons=t()
    studybutton=tkButton(top,'study.ico','study2.ico',260,15,'study',[root,win,studytimes,autostudy,autoreply,icons])
   
   elif 'minus_bo_specialized' in path:
    during_minus=not during_minus
    if during_minus:
     cursor=pyglet.window.ImageMouseCursor(curs[3])
     win.set_mouse_cursor(cursor)
     minusbutton.normalimg=minusbutton.pressimg
     minusbutton.change_scale(1.1)
    else:
     tsprite=pyglet.sprite.Sprite(pyglet.resource.image("minus.ico"),x=win.width-207,y=27)
     minusbutton.normalimg=tsprite
     minusbutton.change_scale(1.1)
   
   elif 'system_bo_specialized' in path:
    top.deiconify()
    top.overrideredirect(True)
   
   elif ('task_' in path) and (path != 'task_none'):
    hwnd=int(path[5:])
    if not during_minus:
     print('task open hwnd=',hwnd)
     win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    else:
     print('task close hwnd=',hwnd)
     win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
   
   elif 'showdias_bo_specialized' in path:
     global showdias
     showdias=not showdias   
   
   elif 'enter_bo_specialized' in path:
      talk()
   
   elif 'timecolor_bo_specialized' in path:
     global timelabelbutton,batterylabel,batterycolor,percentold,stateold
     if timelabelbutton.normalimg.color==darkgray:
      timelabelbutton.normalimg.color=(255,255,255,255)
      batterylabel.color=(255,255,255,255)
      batterycolor='w.png'
      percentold=-1
      stateold=-1
     else:
      timelabelbutton.normalimg.color=darkgray
      batterylabel.color=darkgray
      batterycolor='.png'
      percentold=-1
      stateold=-1
   
   elif 'touch_bo_specialized' in path:
     global girl
     t=path[path.rfind('_')+1:]
     if len(t)>1:
      tt=[]
      for each in t:
       tt.append(int(each)+7)
      ttt=random.randint(0,len(tt)-1)
      tindex=tt[ttt]
     else:
      tindex=int(t)+7
     #print('you touched some part')
     girl = girls[tindex]
     girl._frame_index=1
     girl.x,girl.y=-70,0
     girl.draw()
     rolldias('日和：'+diss[tindex-7],0)
     threading.Thread(target=playgirlvoice_already,args=('touch'+str(tindex),)).start()
   
   elif 'battery_bo_specialized' in path:
     pass
   
   else:
    if not during_minus:
     order='cd '+path[:path.rfind('\\')]+' & '+path[:2]+' & start \"\" \"'+path[path.rfind('\\')+1:]+'\"'
     #print('order=',order)
     os.system(order)
     #print('order finished')
    else:
     iconames,icopaths=[],[]
     iconst=icons
     for icon in icons:
      if icon.path!=path:
       iconames.append(icon.iconame)
       icopaths.append(icon.path)
     t=addicons(win,[])
     icons=t.listicons(iconames,icopaths)
     studybutton=tkButton(top,'study.ico','study2.ico',260,15,'study',[root,win,studytimes,autostudy,autoreply,icons])
     
     
     
def load(win,icons=[]):#读取存在dat中的正常桌面、学习桌面、学习时间段
 global bg_bgname,autostudy,autoreply
 f=open(os.getcwd()+'\\settingsave.dat','r')
 listf=f.readlines()
 iconames,icopaths=[],[]
 for i in range((len(listf)-3)//2):
  icopaths.append(listf[i*2][:len(listf[i*2])-1])
  iconames.append(listf[i*2+1][:len(listf[i*2+1])-1])
 bg_bgname[1]=listf[len(listf)-3][:len(listf[len(listf)-3])-1]
 autostudy=[listf[len(listf)-2][:len(listf[len(listf)-2])-1]]
 autoreply=[listf[len(listf)-1][:len(listf[len(listf)-1])-1]]
 f.close()
 
 times=[]
 f=open(os.getcwd()+'\\studytimesave.dat','r')
 listf=f.readlines()
 for line in listf:
  t=line[:len(line)-1].split()
  times.append([int(t[0]),int(t[1])])
 f.close()
 
 iconames2,icopaths2=[],[]
 f=open(os.getcwd()+'\\studysave.dat','r')
 listf=f.readlines()
 for i in range((len(listf))//2):
  icopaths2.append(listf[i*2][:len(listf[i*2])-1])
  iconames2.append(listf[i*2+1][:len(listf[i*2+1])-1])
 f.close() 
 
 t=addicons(win,[])
 return [t.listicons(iconames,icopaths),times,t.listicons(iconames2,icopaths2)]
 
def save(icons,bg_bgname):#保存正常桌面
 f=open(os.getcwd()+'\\settingsave.dat','w')
 for each in icons: 
  f.write(each.path+'\n')
  f.write(each.iconame+'\n')
 f.write(bg_bgname[1]+'\n')
 f.write(autostudy[0]+'\n')
 f.write(autoreply[0]+'\n')
 f.close()
  

def rolldias(t,who): #实现类似对话记录的界面
 global dias,ldias
 lt=0
 for each in t:
  if ord(each)>256:
   lt+=8.5*1.85
  else:
   lt+=8.5
 lt=int(lt)
 print('lt=',lt)
 if ldias<5:
  dias[ldias].text=t
  if who==1: dias[ldias].x=940-lt
  elif who==0: dias[ldias].x=260
  ldias+=1
 else:
  for i in range(5):
   dias[i].y+=20
  if who==1: dias[0].x=940-lt
  elif who==0: dias[0].x=260
  dias[0].y=70
  dias[0].text=t
  dias=[dias[1],dias[2],dias[3],dias[4],dias[0]]  
    

def talk():  #聊天相关的程序，主要是为了能调用语音
  global dialist,a
  dialist+=document._text[document._text.find('>')+1:]+'\n'
  diat=myname[0]+'：'+document._text[document._text.find('>')+1:]
  rolldias(diat,1)
  #print('diat=',diat)
  rep=a.tulinRobotBuildIn(document._text[document._text.find('>')+1:],during_study)
  for each in rep: 
   rolldias(each,0)
  refreshentry()
  
  drawall()
  win.flip()
  
  def playgirlvoice():
   global voiceplayer
   voicedir = (os.getcwd()+r"\Girlvoice\bin\Girlvoice.exe")
   print(voicedir)
   os.system(voicedir)
   voiceplayer.delete()
   voice = pyglet.media.load('voicefromgirl.wav')
   voiceplayer.queue(voice)
   voiceplayer.play()
  threading.Thread(target=playgirlvoice,args=()).start()
  #print('currentthread during talk=',threading.currentThread())
  
  if '请问需要更换哪一款壁纸呢？' in rep[0]:
   eval('tkuifuncs.'+bgbutton.func)(bgbutton.args)
  if '请自由地调节音量吧~' in rep[0]:
   eval('tkuifuncs.'+musicbutton.func)(musicbutton.args)
  if '好的！但还是先设置一下吧。' in rep[0]:
   eval('tkuifuncs.'+studybutton.func)(studybutton.args)

 
  
def refresh():#刷新所有已经打开的窗口的情况，看看是不是有的名称改了，或者被关闭了
     global lentasks,taskbuttons,titleold,title,hwnds
     title=[]
     count=0
     #while len(title)==0:
     title,hwnds=[],[]
     win32gui.EnumWindows(foo, 0)  
     #print('lentitle=',len(title),'   lenhwnds=',len(hwnds))
     for each in hwndsold: 
      if each in hwnds:
       t=hwnds.index(each)
       del title[t]
       del hwnds[t]

     for i in range(len(title)):
      titleold.append(title[i])
      hwndsold.append(hwnds[i])
      
     #print('lentasks=',lentasks )
     #print('titleold=',titleold)
     #print('hwnds_old=',hwndsold)
     #print('title_after=',title)
     #print('hwnds_after=',hwnds,'\n')
     
     if len(list(title))>0:
      texttitle=list(title)[0]
      if len(texttitle)>27: texttitle=texttitle[:12]+'...'+texttitle[len(texttitle)-12:]
      taskbuttons[lentasks][0].visible=True
      t=w2i.windowtoiconame(hwnds[0])
      if len(t)>0: 
       try: taskbuttons[lentasks][0].normalimg.image=pyglet.resource.image(t+".ico")
       except: print('ico not found')
      taskbuttons[lentasks][0].path='task_'+str(hwnds[0])
      taskbuttons[lentasks][1].visible=True
      taskbuttons[lentasks][1].normalimg.text=texttitle
      taskbuttons[lentasks][1].path='task_'+str(hwnds[0])
      taskbuttons[lentasks][2]=hwnds[0]
      lentasks+=1
  

     taskbuttonst=list(taskbuttons)
     for i in range(len(taskbuttons)):
      taskbutton=taskbuttons[i]
      if taskbutton[0].visible:
       if win32gui.IsWindow(taskbutton[2]) and (win32gui.IsWindowVisible(taskbutton[2]) or win32gui.IsIconic(taskbutton[2])):
        texttitle=win32gui.GetWindowText(taskbutton[2])
        if len(texttitle)>27: texttitle=texttitle[:12]+'...'+texttitle[len(texttitle)-12:]
        taskbutton[1].normalimg.text=texttitle
       else:
        t=i
        #print('close hwnd=',taskbutton[2],' index=',t)
        try:
         hwndsold.remove(taskbuttonst[t][2])
        except:
         pass
        for j in range(t,len(taskbuttons)-1):
         taskbuttonst[j][0].normalimg.image=taskbuttonst[j+1][0].normalimg.image
         taskbuttonst[j][0].path=taskbuttonst[j+1][0].path
         taskbuttonst[j][1].normalimg.text=taskbuttonst[j+1][1].normalimg.text
         taskbuttonst[j][1].path=taskbuttonst[j+1][1].path
         taskbuttonst[j][2]=taskbuttonst[j+1][2]
        taskbuttonst[lentasks-1][0].visible=False
        lentasks-=1
        #taskbutton[1].visible=False
     taskbuttons=list(taskbuttonst)
      

def refreshentry(): #把输入框清空
 global document,layout,caret,win
 document = pyglet.text.document.FormattedDocument('>')
 document.set_style(0,1,{'color':(255,255,255,255),'font_name':'Microsoft Yahei UI','font_size':14})
 layout = pyglet.text.layout.IncrementalTextLayout(document, width=600, height=30)
 layout._set_x(260)
 layout._set_y(23)
 caret = pyglet.text.caret.Caret(layout,None,(255,255,255))
 win.push_handlers(caret)
 win._event_stack[0].pop('on_mouse_press')  
 
 
def drawall(): #画所有的图案
    global ft,bg_bgname,girl
    top.update()
    
    win.clear()
    
    ft=(ft+1)%f
    if ft==0: refresh()
    
    if bg_bgname[1]!=bgbutton.args[0][1]:
     bg_bgname=bgbutton.args[0]
    bg_bgname[0].draw()
    
    docbg.draw()
    if showdias:
     diabg.draw()
     for dia in dias: dia.draw()
    layout.draw()
    for icon in icons:
     icon.draw()
    for eachbutton in l:
     if eachbutton.visible:
      eachbutton.draw()
    for each in taskbuttons:
      if each[0].visible:
       each[0].draw()
       each[1].draw()
    girl.draw()
    if minusbutton.visible: minusbutton.draw()
    showdiasbutton.draw()
    enterbutton.draw()
    
    tiaoshi=False
    if girl._frame_index==len(girl._animation.frames)-1:
     tt=random.randint(1,36)
     if tt>6: tt=7
     #print('gif=',tt)
     girl = girls[tt-1]
     girl.x,girl.y=-70,0
     girl.draw()
     info = psutil.virtual_memory()
     tiaoshi=True
     

    t=list(time.localtime())
    x='%02d'%t[3]+':%02d'%t[4]+':%02d'%t[5]
    timelabelbutton.normalimg.text=x
    timelabelbutton.draw() 
    timestage.draw()
    
    result = ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(powerclass))
    try:     state = int(powerclass.ACLineStatus)
    except:  state = 0 
    
    global percent,percentold,battery,charge,stateold
    percent=int(powerclass.BatteryLifePercent)
    if percentold!=percent:
     percentold=percent
     t='battery'+str((percent-11)//18+1)+batterycolor
     tsprite=pyglet.sprite.Sprite(pyglet.resource.image(t),x=80,y=win.height-55)
     battery.normalimg.delete()
     battery.normalimg=tsprite
     battery.img=battery.normalimg
     battery.change_scale(0.6,0.6)   
     batterylabel.text=str(percent)+'%'
    if stateold!=state:
     stateold=state
     if state==1: t='charge'+batterycolor
     else: t='nocharge'+batterycolor
     tsprite=pyglet.sprite.Sprite(pyglet.resource.image(t),x=163,y=win.height-47)
     charge.normalimg.delete()
     charge.normalimg=tsprite
     charge.img=charge.normalimg
     charge.change_scale(0.35,0.35)       
    
    battery.draw()
    batterylabel.draw()
    charge.draw()
    return tiaoshi
    
    
def playgirlvoice_already(st): #播放预制的语音
      global voiceplayer
      voiceplayer.delete()
      voice = pyglet.media.load('sounds\\'+st+'.wav')
      voiceplayer.queue(voice)
      voiceplayer.play()   
    

#--------------------------------------=各项参数和对象的配置=---------------------   
#print(help(pyglet.sprite.Sprite))   
#t=input()
#win32gui.EnumWindows(fooclear, 0)

pyglet.lib.load_library('avbin')
pyglet.have_avbin=True

pyglet.resource.path=['resources/live2d']
pyglet.resource.reindex()
girls=[]
t=['1x','2x','3x','4x','5x','6x','7x','kanzuoshou','kanyoushou','motou','shakehair','smile','xiong','pangci','stomach']
for each in range(len(t)):
 girls.append(pyglet.sprite.Sprite(pyglet.resource.animation(t[each]+".gif")))
 print(str(each+1)+'/'+str(len(t))+' finished')
girl=girls[0]
girl.x,girl.y=-70,0

screenwidth=GetSystemMetrics(0)
screenheight=GetSystemMetrics(1)
win = w32window.Window(fullscreen=False,caption='看板娘学习桌面',width=screenwidth,height=screenheight)
os.system('taskkill /im explorer.exe /f')
win.set_exclusive_keyboard(True)
'''try:
 os.system('netsh wlan connect PKU')
except: pass'''
bg_bgname=[None,None]
autostudy,autoreply=[],[]
loadt=load(win,[])
icons=loadt[0]
studytimes=loadt[1]
icons2=loadt[2]
title,hwnds=[],[]
win32gui.EnumWindows(foo, 0) 
titleold=title[:]
hwndsold=hwnds[:]
titletasks=[]
black,darkgray= (0,0,0,255),(50,50,50,255)
ft,f=0,20
during_minus,during_study,onemin_study=False,False,False
dialist=''
myname=['波波']
showdias=False
voiceplayer = pyglet.media.Player()
root=tk.Tk()
root.geometry('1x1+3000+2000')
a = buildinchatsys.ChatSys('forever',root,myname[0])
b=[]   
youhua,youhualimit=0,10000
percent,percentold=100,100
stateold=0
batterycolor='.png'
#----------------------------------因为先有window才能调用pyglet，下面是调用pyglet----------------------------#  

@win.event
def on_draw():#每次刷新画面，相当于一个主循环
    global ft,bg_bgname,during_study,onemin_study,icons,icons2,b
    drawall()
    global youhua
    youhua+=1
    if youhua>youhualimit: youhua=youhualimit
    if youhua>youhualimit-2: time.sleep(0.025)
    #print(youhua)
    #print('studytime=',studytimes)
    #print ('内存使用：',psutil.Process(os.getpid()).memory_info().rss)
    #print ('总内存：',info.total)
    #print ('内存占比：',info.percent)
    #print ('cpu个数：',psutil.cpu_count())
    #objgraph.show_growth()
    #print('objgraph.by_type: ',objgraph.by_type('ImageData'))
    #chain =objgraph.find_backref_chain(objgraph.by_type('ImageData')[-1],inspect.ismodule)
    #objgraph.show_chain(chain,filename='test.png')
    #print('autostudy=',autostudy,'    during_study=',during_study)
   
    if a.first[0]==1:
     #print('emergency!!!',a.remark[0],a.index[0])
     b.append(privatechat.privateChat(root,a.remark[0],a.index[0],myname[0],a.emergency,a.firsts,len(b)))
     threading.Thread(target=playgirlvoice_already,args=('emergency',)).start()    
     b[-1].addmessage('-------------------本窗口只能进行文字聊天----------------\n','warn')
     del a.first[0]
     a.first.append(0)
    elif a.currentuser[0]!=None:
     try:
      #print('\nbefore try: ')
      #print(a.currentuser[0])
      #print(a.wins)
      #print(a.currentmsg[0])
      #print(b)
      b[a.currentuser[0]].addmessage(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+'\n','time')
      b[a.currentuser[0]].addmessage(a.wins[a.currentuser[0]]+'：'+a.currentmsg[0]+'\n','msg')
      del a.currentuser[0]
      a.currentuser.append(None)
     except:
      itchat.send(myname[0]+'又去学习了，我是助手日和，如果有急事请输入\'有急事\'，您也可以和我聊天',toUserName=a.index[0])
      a.emergency[0][b[a.currentuser[0]].remark]=False
      a.firsts[0][b[a.currentuser[0]].remark]=False
      del b[a.currentuser[0]]
      del a.wins[a.currentuser[0]]
      del a.currentuser[0]
      a.currentuser.append(None)
      #print('\nafter expect: ')
      #print(a.currentuser[0])
      #print(a.wins)
      #print(a.currentmsg[0])
      #print(b)
      
    flagf,flag2=False,False
    t=list(time.localtime())
    old=-1
    timenow=t[3]*60+t[4]
    for timet in studytimes:
     if timet[0]<=timenow<=timet[1]:
      flagf=False
      onemin_study=False
      flag2=True
      timestage.text='%02d'%(timet[0]//60)+':'+'%02d'%(timet[0]%60)+' — '+'%02d'%(timet[1]//60)+':'+'%02d'%(timet[1]%60)
      if autostudy[0]=='1':
       flagf=True
       if not during_study:
        if minusbutton.visible:
         settingbutton.change_scale(3.3-settingbutton.smallscale,1.8)
         settingbutton.dx,settingbutton.dy=4-settingbutton.dx,3-settingbutton.dy     
        #print('it\'s study time')
        for each in range(1,len(l)): 
         l[each].visible=False
        minusbutton.visible=False
        rolldias('日和：'+myname[0]+'，该开始学习啦！',0)
        threading.Thread(target=playgirlvoice_already,args=('studynow',)).start()
        f=open('C:\\Windows\\System32\\drivers\\etc\\hosts1','r')
        listf=f.readlines()
        f.close()
        f=open('C:\\Windows\\System32\\drivers\\etc\\hosts','w')
        for each in listf: f.write(each)
        f.close()
        iconames2,icopaths2=[],[]
        f=open(os.getcwd()+'\\studysave.dat','r')
        listf=f.readlines()
        f.close()
        for i in range(len(listf)//2):
          icopaths2.append(listf[i*2][:len(listf[i*2])-1])
          iconames2.append(listf[i*2+1][:len(listf[i*2+1])-1])
          t=addicons(win,[])
          icons2=t.listicons(iconames2,icopaths2)
        icons,icons2=icons2,icons
        if autoreply[0]=='1': 
         if itchat.check_login()!='200':
          a.timeconfirm()
         else:
          a.start()
          
      elif not during_study:
       print('已经是学习时间了')
      break
     elif (timenow==timet[0]-1) and not onemin_study:
      onemin_study=True
      rolldias('日和：'+myname[0]+'，1分钟后就要开始学习啦！',0)
      threading.Thread(target=playgirlvoice_already,args=('1minstudy',)).start()
     elif old<timenow<timet[0]:
      flag2=True
      timestage.text=' next   '+'%02d'%(timet[0]//60)+':'+'%02d'%(timet[0]%60)+' '
     old=timet[1]
    if during_study and not flagf:   
      rolldias('日和：'+myname[0]+'，学习时间结束了，微信托管已经暂停，放松一下吧~',0)
      threading.Thread(target=playgirlvoice_already,args=('relaxnow',)).start()   
      f=open('C:\\Windows\\System32\\drivers\\etc\\hosts','w')
      f.close()
      icons,icons2=icons2,icons      
      if autoreply[0]=='1': 
       a.stop()
    if flagf: during_study=True
    else :during_study=False
    if not flag2 and not during_study: timestage.text=''
    
    gc.collect()

  
@win.event
def on_key_press(symbol,modif): #实现回车发送消息
 if symbol==key.ENTER:
  talk()
    
    
@win.event
def on_mouse_motion(x,y,button,modif): #鼠标移动，实现按钮的动画    
    for icon in icons:
     icon.collide(x,y+24)
    if not during_minus:
     showdiasbutton.collide(x,y+24)
     enterbutton.collide(x,y+24)
     for eachbutton in l:
      eachbutton.collide(x,y+24)
    for each in taskbuttons:
     if each[0].visible:  
      if not each[0].collide(x,y+24)[0]:
       each[1].collide(x,y+24)
    minusbutton.collide(x,y+24)
    

@win.event
def on_mouse_press(x,y,button,modif):  #实现所有鼠标点击的效果，并call前面的exe函数
    global win,youhua
    youhua=0
    if button==mouse.LEFT:
        #print('mouse left was pressed!')
        
        for icon in icons:
         t=icon.collide(x,y+24)
         if t[0]: exe(t[1])
         
        if not during_minus:
         t=timelabelbutton.collide(x,y+24)
         if t[0]: exe(t[1])
         t=showdiasbutton.collide(x,y+24)
         if t[0]: exe(t[1])
         t=enterbutton.collide(x,y+24)
         if t[0]: exe(t[1])
         cursor=pyglet.window.ImageMouseCursor(curs[1])
         win.set_mouse_cursor(cursor)
         if not during_study:
          for eachbutton in l:
           t=eachbutton.collide(x,y+24)
           if t[0] and eachbutton.visible: exe(t[1])
        
        if not during_study:
         t=minusbutton.collide(x,y+24)
         if t[0] and minusbutton.visible: exe(t[1])
        
        for eachtask in taskbuttons:
         if eachtask[0].visible:
          t1=eachtask[0].collide(x,y+24)
          t2=eachtask[1].collide(x,y+24)
          if t1[0]:exe(t1[1])
          if t2[0]:exe(t2[1])
        
        for eachpart in touchs:
         t=eachpart.collide(x,y+24)
         if t[0]: exe(t[1])
    elif button==mouse.RIGHT:
        #print('mouse right was pressed!')
        cursor=pyglet.window.ImageMouseCursor(curs[2])
        win.set_mouse_cursor(cursor)
        #addicons()
    elif button==mouse.MIDDLE:
        #print('mouse middle was pressed!')
        pass
        

@win.event
def on_mouse_release(x,y,button,modif): #换个鼠标指针
   if not during_minus:
    cursor=pyglet.window.ImageMouseCursor(curs[0])
    win.set_mouse_cursor(cursor)
		


#/--------------------------------------下面读入一些图片--------------------------------------------------/#

pyglet.resource.path=['resources/wallpapers']
pyglet.resource.reindex()
bg_bgname[0]=pyglet.sprite.Sprite(pyglet.resource.image(bg_bgname[1]))
bg_bgname[0].update(scale_x=win.width/bg_bgname[0].width,scale_y=win.height/bg_bgname[0].height)


pyglet.resource.path=['resources/cursors']
pyglet.resource.reindex()
curs=[]
for i in range(4):
 curs.append(pyglet.resource.image("cur"+str(i+1)+".png"))
 


if ctypes.windll.shell32.IsUserAnAdmin(): #关闭调试界面 
 #print('is admin')  
 whnd = ctypes.windll.kernel32.GetConsoleWindow()
 if whnd != 0:  ctypes.windll.user32.ShowWindow(whnd, 0)


 
#/################################ 下面建立一些要用到的tkinter的button########################################/#
top=tk.Toplevel(root)
top.geometry('500x120+'+str(win.width//2-250)+'+'+str(win.height//2-60))

def overrideiconify():
  top.overrideredirect(False)
  top.iconify() 
 
closebutton=tk.Button(top,bd=0,font=('Microsoft Yahei UI',14),activeforeground='red',fg='black',text='返 回',command=overrideiconify)
canvas=tk.Canvas(top,width=500,height=120,bd=0)
closebutton.place(x=230,y=80)

bgbutton=tkButton(top,'bg.ico','bg2.ico',20,15,'changebg',[bg_bgname,win])
musicbutton=tkButton(top,'sound.ico','sound2.ico',100,15,'sndvol',[])
wifibutton=tkButton(top,'wifi.ico','wifi2.ico',180,15,'wifi',[root,win])
studybutton=tkButton(top,'study.ico','study2.ico',260,15,'study',[root,win,studytimes,autostudy,autoreply,icons])
codebutton=tkButton(top,'code.ico','code2.ico',340,15,'console',[])
otherbutton=tkButton(top,'other.ico','other2.ico',420,15,'other',[root,win,myname])

top.iconify()


#/##################################### 下面是可以在桌面上看到的buttons###########################################/#
cursor=pyglet.window.ImageMouseCursor(curs[0])
win.set_mouse_cursor(cursor)
pyglet.resource.path=['resources']
pyglet.resource.reindex()
taskbuttons,lentasks=[],0
for i in range(12):
 for j in range(2):
  tsprite=pyglet.sprite.Sprite(pyglet.resource.image("blank.ico"),x=300+j*340,y=win.height-100-40*i)
  tbutton=Button(tsprite,None,'task_none',None,0,tsprite.x,tsprite.x+32,tsprite.y,tsprite.y+32)
  tbutton.change_scale(0.8,1)
  tbutton.visible=False
  tlabel=pyglet.text.Label('1234567890abcdefghijkl',font_name='Microsoft Yahei UI',font_size=12,x=tsprite.x+34,y=tsprite.y+6,color=black)
  labelbutton=Button(tlabel,None,'task_none',None,0,tlabel.x,tlabel.x+13*len(tlabel.text),tlabel.y,tlabel.y+20)
  labelbutton.change_scale(12,14)
  labelbutton.visible=False
  tbutton.set_relative(labelbutton)
  labelbutton.set_relative(tbutton)
  taskbuttons.append([tbutton,labelbutton,-1234567])
  
  
tsprite=pyglet.sprite.Sprite(pyglet.resource.image("setting.ico"),x=win.width-76,y=24)
settingbutton=Button(tsprite,None,'setting_bo_specialized',None,0,tsprite.x,tsprite.x+48,tsprite.y,tsprite.y+48)
settingbutton.dx,settingbutton.dy=4,3
settingbutton.change_scale(1.5,1.8)
tsprite=pyglet.sprite.Sprite(pyglet.resource.image("turnoff.ico"),x=win.width-123,y=27)
tsprite2=pyglet.sprite.Sprite(pyglet.resource.image("turnoff2.ico"),x=win.width-123,y=27)
turnoffbutton=Button(tsprite,tsprite2,'turnoff_bo_specialized',None,0,tsprite.x,tsprite.x+35,tsprite.y,tsprite.y+35)
turnoffbutton.change_scale(1.1)
tsprite=pyglet.sprite.Sprite(pyglet.resource.image("add.ico"),x=win.width-165,y=27)
tsprite2=pyglet.sprite.Sprite(pyglet.resource.image("add2.ico"),x=win.width-165,y=27)
addbutton=Button(tsprite,tsprite2,'add_bo_specialized',None,0,tsprite.x,tsprite.x+35,tsprite.y,tsprite.y+35)
addbutton.change_scale(1.1) 
tsprite=pyglet.sprite.Sprite(pyglet.resource.image("minus.ico"),x=win.width-207,y=27)
tsprite2=pyglet.sprite.Sprite(pyglet.resource.image("minus2.ico"),x=win.width-207,y=27)
minusbutton=Button(tsprite,tsprite2,'minus_bo_specialized',None,0,tsprite.x,tsprite.x+35,tsprite.y,tsprite.y+35)
minusbutton.change_scale(1.1)
tsprite=pyglet.sprite.Sprite(pyglet.resource.image("system.ico"),x=win.width-252,y=25)
tsprite2=pyglet.sprite.Sprite(pyglet.resource.image("system2.ico"),x=win.width-252,y=25)
systembutton=Button(tsprite,tsprite2,'system_bo_specialized',None,0,tsprite.x,tsprite.x+35,tsprite.y,tsprite.y+35)
systembutton.change_scale(1.2)
for each in [turnoffbutton,addbutton,minusbutton,systembutton]: each.visible=False

t=list(time.localtime())
x='%02d'%t[3]+':%02d'%t[4]+':%02d'%t[5]
timelabel=pyglet.text.Label(x,font_name='Microsoft Yahei UI',font_size=20,x=75,y=win.height-70,color=darkgray)
timelabelbutton=Button(timelabel,None,'timecolor_bo_specialized',None,0,timelabel.x,timelabel.x+20*len(timelabel.text),timelabel.y-5,timelabel.y+20)
timelabelbutton.change_scale(20,20)
timestage=pyglet.text.Label('asfadsfafads',font_name='Microsoft Yahei UI',font_size=14,x=69,y=win.height-90,color=(100,0,0,200))
tsprite=pyglet.sprite.Sprite(pyglet.resource.image("battery5.png"),x=80,y=win.height-55)
battery=Button(tsprite,None,'battery_bo_specialized',None,0,tsprite.x,tsprite.x+36,tsprite.y,tsprite.y+36)
battery.change_scale(0.6,0.6)
batterylabel=pyglet.text.Label('100%',font_name='Microsoft Yahei UI',font_size=10,x=125,y=win.height-43,color=darkgray)
tsprite=pyglet.sprite.Sprite(pyglet.resource.image("nocharge.png"),x=163,y=win.height-47)
charge=Button(tsprite,None,'battery_bo_specialized',None,0,tsprite.x,tsprite.x+36,tsprite.y,tsprite.y+36)
charge.change_scale(0.35,0.35)


l=[settingbutton,turnoffbutton,addbutton,systembutton]


docbg=pyglet.sprite.Sprite(pyglet.resource.image("docbg.png"),x=250,y=25)
docbg.update(scale_x=700/docbg.width,scale_y=30/docbg.height)
diabg=pyglet.sprite.Sprite(pyglet.resource.image("diabg.png"),x=250,y=54)
diabg.update(scale_x=700/diabg.width,scale_y=120/diabg.height)
dias=[]
dias.append(pyglet.text.Label('日和：你好呀~',font_name='Microsoft Yahei UI',font_size=12,x=260,y=150,color=(255,255,255,255)))
for i in range(4): dias.append(pyglet.text.Label('',font_name='Microsoft Yahei UI',font_size=12,x=750-490*(i%2),y=130-20*i,color=(255,255,255,255)))
ldias=1
tsprite=pyglet.sprite.Sprite(pyglet.resource.image("showdias.ico"),x=880,y=31)
tsprite2=pyglet.sprite.Sprite(pyglet.resource.image("showdias2.ico"),x=880,y=31)
showdiasbutton=Button(tsprite,tsprite2,'showdias_bo_specialized',None,0,tsprite.x,tsprite.x+23,tsprite.y,tsprite.y+23)
showdiasbutton.change_scale(0.9)
tsprite=pyglet.sprite.Sprite(pyglet.resource.image("enter.ico"),x=910,y=27)
tsprite2=pyglet.sprite.Sprite(pyglet.resource.image("enter2.ico"),x=910,y=27)
enterbutton=Button(tsprite,tsprite2,'enter_bo_specialized',None,0,tsprite.x,tsprite.x+23,tsprite.y,tsprite.y+23)
enterbutton.change_scale(1.1)
refreshentry()


touchs=[]
places=[(8.61,10.3,10.3,13.18,1),(4.02,5.54,10.3,13.18,1),(5.43,8.47,17.25,21.05,3),(5.43,8.47,17.25,21.05,3),(5.43,8.47,17.25,21.05,3),(5.79,8.36,14.46,16.02,1),(5.36,8.78,9.03,11.18,1),(5.96,8.22,11.64,13.48,1)]
diss=['咦，手怎么了吗？','咦，手怎么了吗？','唔，感觉，好舒服','呀，头发都乱了','嘿嘿……','噫！你这个绅~士~','走开，坏人！','啊！吓了我一跳']
tsprite=pyglet.sprite.Sprite(pyglet.resource.image("blank.ico"),x=100000,y=100000)
tplace=lambda x: int(x*384/13.55-70)
i=0
while i<8:
 t=''
 if places[i][4]==1:
  t=str(i)
 else:
  for j in range(places[i][4]):
   t=t+str(i+j)
 touchs.append(Button(tsprite,None,'touch_bo_specialized_'+t,None,0,tplace(places[i][0]),tplace(places[i][1]),tplace(places[i][2])+70,tplace(places[i][3])+70)) 
 i+=places[i][4]



pyglet.app.run()
