from tkinter import *
from tkinter import ttk
from xmlrpc import client
from tkinter import messagebox
import yaml
import time
import threading
import os

#author wbyu123
root = Tk()
root.title("BLOG 日志发送器")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)


url = StringVar()  #服务器地址
method = StringVar()  #远程方法名
title=StringVar()   #标题
category=StringVar()   #类别
englishname=StringVar()   #英文名




f = open('config.yaml')
# use safe_load instead load
dataMap = yaml.safe_load(f)

f = open('config.yaml')
# use safe_load instead load
dataMap = yaml.safe_load(f)

url.set(dataMap['url'])
method.set(dataMap['method'])


ttk.Label(mainframe, text="服务器地址:").grid(column=0, row=1, sticky=E)
feet_entry = ttk.Entry(mainframe, width=17, textvariable=url)
feet_entry.grid(column=1, row=1, sticky=(W, E))

ttk.Label(mainframe, text="远程方法名:").grid(column=2, row=1, sticky=E)
feet_entry = ttk.Entry(mainframe, width=12, textvariable=method)
feet_entry.grid(column=3, row=1, sticky=(W, E))

ttk.Label(mainframe, text="类别:").grid(column=0, row=2, sticky=E)
w = ttk.Combobox(mainframe, textvariable=category, values=list(dataMap['categorys'].keys()))
w.grid(column=1, row=2, sticky=(W, E))

ttk.Label(mainframe, text="别名:").grid(column=2, row=2, sticky=E)
feet_entry = ttk.Entry(mainframe, width=5, textvariable=englishname)
feet_entry.grid(column=3, row=2, sticky=(W, E))


codenum=StringVar()   #代码
ttk.Label(mainframe, text="插入代码:").grid(column=0, row=3, sticky=E)
codeinsert = ttk.Combobox(mainframe, textvariable=codenum)
codeinsert['values'] = ('css', 'javascript', 'python','php')
codeinsert.state(['readonly'])

codeinsert.grid(column=1, row=3, sticky=(W, E))

ttk.Label(mainframe, text="标题:").grid(column=0, row=4, sticky=E)
feet_entry = ttk.Entry(mainframe, width=17, textvariable=title)
feet_entry.grid(column=1, columnspan=3,row=4, sticky=(W, E))

ttk.Label(mainframe, text="内容:").grid( column=0,row=5, sticky=E)

content = Text(mainframe, width=70, height=40)
content.grid(column=1,columnspan=3,row=5, sticky=(W, E))



def send():
    global id
    try:
        proxy = client.ServerProxy(url.get())
        categoryid=dataMap['categorys'][category.get()]
        script="proxy.{0}(title.get(),content.get(1.0,END),categoryid,englishname.get())".format(method.get());
        result = exec(script)
        histroyblogs[id]['status'] = '1'
        writehistroyblogs()
        messagebox.showinfo(message='发送成功')
    except Exception as inst:
        strg="发送失败:"+ str(inst)
        messagebox.showinfo(message=strg)

def insercode(*args):
    content.insert(END,'\n<pre class="{0}" name="code">\n\n</pre>'.format(codenum.get()))

if not os.path.exists("data"):
    os.mkdir("data")

if not os.path.exists("blogs.yaml"):
    open('blogs.yaml','w')
    
#历史保留的博客  
blogsfile = open('blogs.yaml','r')
histroyblogs =  yaml.safe_load(blogsfile)

id=-1
def autosave():
    global id,histroyblogs
     #每1分钟保存一次
    #为它生成一个新的id
    if id==-1:
        id=str(time.time()).replace('.','')
        print(id)
        if histroyblogs is None:
           histroyblogs=dict()
    while 1:
      time.sleep(10) 
      if histroyblogs.get(id) is None: 
        histroyblogs[id] =dict() 
      histroyblogs[id]['title']=title.get()
      histroyblogs[id]['status'] = '0'
      histroyblogs[id]['englishname'] = englishname.get()
      writehistroyblogs()
      writecontent()

def writehistroyblogs():
    global histroyblogs
    blogsfile = open('blogs.yaml','w')
    yaml.dump(histroyblogs,blogsfile)
    blogsfile.close()

def writecontent():
    global id
    datafile = open("data/"+id,"w")
    datafile.write(content.get(1.0,END))    
    datafile.close()


autosavethread = threading.Thread(target=autosave)       
autosavethread.start()

    
codeinsert.bind('<<ComboboxSelected>>', insercode)
ttk.Button(mainframe, text="发送", command=send).grid(column=2, row=6, sticky=(W, E))

root.mainloop()