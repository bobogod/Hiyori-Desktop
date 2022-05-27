import pyglet
import os
import w32window
import tkinter as tk
from tkuifuncs import *

class Button:
 def __init__(self,normalimg,pressimg,path,iconame,collidertype,*argv): #鼠标移动上去一种是图标放大，一种是换图标，给定判定域，给定按钮相关的函数和程序的path
  self.normalimg=normalimg
  self.path=path
  self.iconame=iconame
  self.collidertype=collidertype
  self.collider=argv
  self.pressimg=pressimg
  self.img=self.normalimg
  self.incollider=False
  self.visible=True
  self.smallscale=1.5
  self.bigscale=1.8
  self.normalimg.scale=self.smallscale
  self.dx=5
  self.dy=3
  if self.pressimg!=None: self.pressimg.scale=self.smallscale
  self.relative=None
 
 def change_scale(self,small=1.5,big=1.8):#方便改变参数
  self.smallscale=small
  self.bigscale=big
  if type(self.normalimg)==type(pyglet.text.Label()):
   self.normalimg.font_size=self.smallscale
  else:
   self.normalimg.scale=self.smallscale
  if self.pressimg!=None: self.pressimg.scale=self.smallscale
  
  
 def collide(self,x,y):#碰撞检测
  if self.collidertype==0:
   if self.collider[0]<x<self.collider[1] and self.collider[2]<y<self.collider[3]: 
    if not self.incollider: self.on_press()
    self.incollider=True
    if self.relative!=None:
     if not self.relative.incollider: self.relative.on_press()
     self.relative.incollider=True
    return [True,self.path]
   else: 
    if self.incollider: self.on_release()
    self.incollider=False
    if self.relative!=None:
     if self.relative.incollider: self.relative.on_release()
     self.relative.incollider=False
    return [False,None]
  elif self.collidertype==1:
   pass
  
 def on_press(self):  #碰到的动画
   if self.pressimg==None:
    if type(self.normalimg)==type(pyglet.text.Label()):
     self.normalimg.font_size=self.bigscale
    else:
     self.normalimg.scale=self.bigscale
     self.normalimg.x-=self.dx
     self.normalimg.y-=self.dy
     self.img=self.normalimg
   else:
    self.img=self.pressimg
 
 def on_release(self): #移出的动画
  if self.pressimg==None:
   if type(self.normalimg)==type(pyglet.text.Label()):
     self.normalimg.font_size=self.smallscale
   else:
    self.normalimg.scale=self.smallscale
    self.normalimg.x+=self.dx
    self.normalimg.y+=self.dy
    self.img=self.normalimg
  else:
   self.img=self.normalimg
   
 
 def draw(self):
  self.img.draw()
  
 def set_relative(self,other):
  self.relative=other
  
  
  
  
class tkButton:
 def __init__(self,top,image1,image2,xx,yy,func,args):  #美化了tkinter的button，加了切换图片的动画
 
  def change1(buttonevent):
   if buttonevent.type==tk.EventType.Enter:
    self.button1.place(x=3000+xx,y=yy)
    self.button2.place(x=xx,y=yy)
  
  def change2(buttonevent):
   if buttonevent.type==tk.EventType.ButtonRelease:
    eval('tkuifuncs.'+self.func)(args)  #直接call tkuifuncs里面对应的函数
   elif buttonevent.type==tk.EventType.Leave:
    self.button2.place(x=3000+xx,y=yy)
    self.button1.place(x=xx,y=yy)
 
  self.args=args
  self.img=tk.PhotoImage(file='resources/'+image1)
  self.button1=tk.Label(top,image=self.img)
  self.button1.bind('<ButtonRelease-1>',change1)
  self.button1.bind('<Enter>',change1)
  self.button1.place(x=xx,y=yy)
  self.img2=tk.PhotoImage(file='resources/'+image2)
  self.button2=tk.Label(top,image=self.img2)
  self.button2.bind('<ButtonRelease-1>',change2)
  self.button2.bind('<Leave>',change2)
  self.button2.place(x=3000+xx,y=yy)
  self.func=func