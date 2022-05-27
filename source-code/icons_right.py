import pyglet
import os
from pyglet.window import mouse
import w32window
from tkinter import filedialog
import tkinter as tk
from MyButton import *

class addicons:
 def __init__(self,win,icons):
  self.win=win
  self.icons=icons
  #print('len=',len(self.icons))
  pyglet.resource.path=['resources']
  pyglet.resource.reindex()
 
 def __call__(self):
  filenames=list(filedialog.askopenfilenames(filetypes=[('EXE','*.exe')]))      #获得路径列表
  print(filenames)

  for i in range(len(filenames)):                      #处理路径格式
   for j in range(len(filenames[i])):
    if filenames[i][j]=='/':
     filenames[i]=filenames[i][:j]+'\\'+filenames[i][j+1:] 

  filenamesnew=[]
  for i in range(len(filenames)): 
   filename=filenames[i][:len(filenames[i])-4]
   filenamenew=''
   for each in filename:
    if each=='\\':  filenamenew+='_'             #形成ico文件名
    elif each!=':':  filenamenew+=each
   filenamesnew.append(filenamenew)
  print(filenamesnew)
 
  paths,filenames=filenames,[]
  for i in range(len(filenamesnew)):         #优化已有的ico
   if not os.path.exists("resources\\"+filenamesnew[i]+".ico"):
    filenames.append(paths[i])
  print(filenames)
   
  f=open(os.getcwd()+'\\resources\\form.dat','w')
  for each in filenames:                     #写入共享文件
   f.write(each+'\n')
  f.close()
   
  os.system('cd resources & toico.exe')
  #self.win.set_fullscreen(fullscreen=True)
  pyglet.resource.path=['resources']
  pyglet.resource.reindex()
  iconsoldpaths,iconsoldiconames=[],[]
  for each in self.icons:
   iconsoldpaths.append(each.path)
   iconsoldiconames.append(each.iconame)
  iconsnewpaths=sorted(set(iconsoldpaths+paths))
  iconsnewiconames=sorted(set(iconsoldiconames+filenamesnew))
  return self.listicons(iconsnewiconames,iconsnewpaths)
  
 def listicons(self,iconsnewiconames,iconsnewpaths):  #把icons排版
  gap,settingy=24,36
  iconsnew=[]
  for i in range(len(iconsnewiconames)):
   if 17>len(iconsnewiconames)>8:
    if i<8:
     try:
      tsprite=pyglet.sprite.Sprite(pyglet.resource.image(iconsnewiconames[i]+".ico"),x=self.win.width-72,y=settingy+self.win.height//2-24+(24+gap//2)*7-(48+gap)*i)
     except: print('ico not found')
    else:
     try:
      tsprite=pyglet.sprite.Sprite(pyglet.resource.image(iconsnewiconames[i]+".ico"),x=self.win.width-160,y=settingy+self.win.height//2-24+(24+gap//2)*(len(iconsnewiconames)-9)-(48+gap)*(i-8))
     except: print('ico not found')
   elif len(iconsnewiconames)>16:
    if i<8:
     try:
      tsprite=pyglet.sprite.Sprite(pyglet.resource.image(iconsnewiconames[i]+".ico"),x=self.win.width-72,y=settingy+self.win.height//2-24+(24+gap//2)*7-(48+gap)*i)
     except: print('ico not found')
    elif i<16:
     try:
      tsprite=pyglet.sprite.Sprite(pyglet.resource.image(iconsnewiconames[i]+".ico"),x=self.win.width-160,y=settingy+self.win.height//2-24+(24+gap//2)*7-(48+gap)*(i-8))
     except: print('ico not found')
    else:
     try:
      tsprite=pyglet.sprite.Sprite(pyglet.resource.image(iconsnewiconames[i]+".ico"),x=self.win.width-248,y=settingy+self.win.height//2-24+(24+gap//2)*(len(iconsnewiconames)-17)-(48+gap)*(i-16))
     except: print('ico not found')
   else:
    try:
     tsprite=pyglet.sprite.Sprite(pyglet.resource.image(iconsnewiconames[i]+".ico"),x=self.win.width-72,y=settingy+self.win.height//2-24+(24+gap//2)*(len(iconsnewiconames)-1)-(48+gap)*i)
    except: print('ico not found')
   iconsnew.append(Button(tsprite,None,iconsnewpaths[i],iconsnewiconames[i],0,tsprite.x,tsprite.x+48,tsprite.y,tsprite.y+48))
  return iconsnew