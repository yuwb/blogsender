from tkinter import *
from tkinter import ttk
from xmlrpc import client
from tkinter import messagebox
import yaml
import time
import threading
import os

#author wbyu123
def send():
    global id,status
    try:
        proxy = client.ServerProxy(url.get())
        categoryid=dataMap['categorys'][category.get()]
        if status!='1':
         result=proxy.newPost(title.get(),content.get(1.0,END),categoryid,englishname.get(),publishweibo.get())
        else:
         result=proxy.updatePost(title.get(),content.get(1.0,END),categoryid,englishname.get())
        histroyblogs[id]['status'] = '1'
        status='1'
        publicstatus.set(publicstatusmessages[status])
        writehistroyblogs()
        messagebox.showinfo(message='发送成功')
    except Exception as inst:
        strg="发送失败:"+ str(inst)
        messagebox.showinfo(message=strg)

def insercode(*args):
    if codenum.get()=='img':
        content.insert(INSERT,'\n<img src=""  height="460" width="478" /><br>')
    else:
        content.insert(INSERT,'\n<pre class="{0}" name="code">\n\n</pre>'.format(codenum.get()))


def autosave():
     #每1分钟保存一次
    #为它生成一个新的id
    while 1:
      time.sleep(10) 
      save()

def save():
    global id,histroyblogs
    if(title.get()):
      if id==-1:
         id=str(time.time()).replace('.','')
         histroyblogs[id]=dict()
         histroyblogs[id]['status'] = '0'
      histroyblogs[id]['title']=title.get()
      histroyblogs[id]['englishname'] = englishname.get()
      histroyblogs[id]['category'] = category.get()
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

def selectblog(*args):
    global id,blogtitle,histroyblogs,status
    for val in  histroyblogs.keys():
        if histroyblogs.get(val).get('title')==blogtitle.get():
            id=val;
            title.set(blogtitle.get())
            englishname.set(histroyblogs.get(val).get('englishname'))
            category.set(histroyblogs.get(val).get('category'))
            status=histroyblogs.get(val).get('status')
            publicstatus.set(publicstatusmessages[status])
            datafile = open("data/"+id,"r")
            content.delete(0.0,END)
            content.insert(0.0,datafile.read())
            datafile.close()
            break;

            
def delete():
    global id,status
    if status=='1':
        try:
            proxy = client.ServerProxy(url.get())
            proxy.deletePost(englishname.get())
            histroyblogs[id]['status']='2'
            status='2'
            writehistroyblogs()
            publicstatus.set(publicstatusmessages[status])
            messagebox.showinfo(message='删除成功')
        except Exception as inst:
            strg="删除失败:"+ str(inst)
            messagebox.showinfo(message=strg)
    else:
        messagebox.showinfo(message="该博客未发布过")
    

if __name__ == "__main__":
    
    root = Tk()
    root.title("BLOG 日志发送器")
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    url = StringVar()  #服务器地址
    title=StringVar()   #标题
    category=StringVar()   #类别
    englishname=StringVar()   #英文名
    publicstatus=StringVar()   #发布状态
    publicstatus.set("未发布")
    id=-1
    status='0'
    publishweibo=StringVar()  #是否发微博
    publishweibo.set("0")   #默认不发


    f = open('config.yaml')
    # use safe_load instead load
    dataMap = yaml.safe_load(f)
    url.set(dataMap['url'])
    
    if not os.path.exists("data"):
        os.mkdir("data")

    if not os.path.exists("blogs.yaml"):
        open('blogs.yaml','w')


    ttk.Label(mainframe, text="服务器地址:").grid(column=0, row=1, sticky=E)
    feet_entry = ttk.Entry(mainframe, width=17, textvariable=url)
    feet_entry.grid(column=1, row=1, sticky=(W, E))

    ttk.Label(mainframe, text="发布状态:").grid(column=2, row=1, sticky=E)
    ttk.Label(mainframe, textvariable=publicstatus).grid(column=3, row=1, sticky=W)

    ttk.Label(mainframe, text="类别:").grid(column=0, row=2, sticky=E)
    categorytag = ttk.Combobox(mainframe, textvariable=category, values=list(dataMap['categorys'].keys()))
    categorytag.grid(column=1, row=2, sticky=(W, E))

    ttk.Label(mainframe, text="别名:").grid(column=2, row=2, sticky=E)
    feet_entry = ttk.Entry(mainframe, width=5, textvariable=englishname)
    feet_entry.grid(column=3, row=2, sticky=(W, E))


    codenum=StringVar()   #代码
    ttk.Label(mainframe, text="插入代码:").grid(column=0, row=3, sticky=E)
    codeinsert = ttk.Combobox(mainframe, textvariable=codenum)
    codeinsert['values'] = ('css', 'javascript', 'python','php','img')
    codeinsert.state(['readonly'])
    codeinsert.grid(column=1, row=3, sticky=(W, E))
    codeinsert.bind('<<ComboboxSelected>>', insercode)

    #历史保留的博客  
    blogsfile = open('blogs.yaml','r')
    histroyblogs =  yaml.safe_load(blogsfile)
    if histroyblogs is None:
       histroyblogs=dict()
  
    bloglist=[]
    for val in  histroyblogs.values():  
        bloglist.append(val.get('title'))


    blogtitle=StringVar()   #历史文章列表
    ttk.Label(mainframe, text="文章列表:").grid(column=2, row=3, sticky=E)
    blogs = ttk.Combobox(mainframe, textvariable=blogtitle)
    blogs['values'] = bloglist
    blogs.state(['readonly'])
    blogs.grid(column=3, row=3, sticky=(W, E))
    blogs.bind('<<ComboboxSelected>>', selectblog)
    

    ttk.Label(mainframe, text="标题:").grid(column=0, row=4, sticky=E)
    feet_entry = ttk.Entry(mainframe, width=17, textvariable=title)
    feet_entry.grid(column=1, columnspan=2,row=4, sticky=(W, E))
    
    ttk.Label(mainframe, text="是否发微博:").grid(column=3, row=4, sticky=W)
    weibo_pubulish = ttk.Combobox(mainframe,width=10, textvariable=publishweibo,values=['0','1'])
    weibo_pubulish.grid(column=3, row=4, sticky=E)
    
    ttk.Label(mainframe, text="内容:").grid( column=0,row=5, sticky=E)

    content = Text(mainframe, width=70, height=40)
    content.grid(column=1,columnspan=3,row=5, sticky=(W, E))
    publicstatusmessages={'1':'已发布','0':'未发布','2':'已删除'}
    
    autosavethread = threading.Thread(target=autosave)       
    autosavethread.start()
  
    
    ttk.Button(mainframe, text="发送", command=send).grid(column=1, row=6, sticky=(W, E))
    ttk.Button(mainframe, text="保存", command=save).grid(column=2, row=6, sticky=(W, E))
    ttk.Button(mainframe, text="删除", command=delete).grid(column=3, row=6, sticky=(W, E))

    root.mainloop()