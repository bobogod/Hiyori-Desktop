import win32api,win32con,win32process,win32gui

def windowtoiconame(hwnd):#根据窗口句柄获得ico和name
 try:
  t=win32process.GetWindowThreadProcessId(hwnd)
  hprocess=win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS,False,t[1])
  st=win32process.GetModuleFileNameEx(hprocess,0)
 except:
  print('error in win2ico')
  st='xxxx'
 
 st=st[:len(st)-4]
 stnew=''
 for each in st:
  if each=='\\':  stnew+='_'             #形成ico文件名
  elif each!=':':  stnew+=each
 
 return stnew
 
