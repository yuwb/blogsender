from tkinter import *
from tkinter import ttk
import xmlrpc.client
from tkinter import messagebox
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
content=StringVar()   #内容


ttk.Label(mainframe, text="服务器地址:").grid(column=0, row=1, sticky=E)
feet_entry = ttk.Entry(mainframe, width=17, textvariable=url)
feet_entry.grid(column=1, row=1, sticky=(W, E))

ttk.Label(mainframe, text="远程方法名:").grid(column=2, row=1, sticky=E)
feet_entry = ttk.Entry(mainframe, width=12, textvariable=method)
feet_entry.grid(column=3, row=1, sticky=(W, E))

ttk.Label(mainframe, text="类别:").grid(column=0, row=2, sticky=E)
feet_entry = ttk.Entry(mainframe, width=5, textvariable=category)
feet_entry.grid(column=1, row=2, sticky=(W, E))

ttk.Label(mainframe, text="别名:").grid(column=2, row=2, sticky=E)
feet_entry = ttk.Entry(mainframe, width=5, textvariable=englishname)
feet_entry.grid(column=3, row=2, sticky=(W, E))


ttk.Label(mainframe, text="标题:").grid(column=0, row=3, sticky=E)
feet_entry = ttk.Entry(mainframe, width=17, textvariable=title)
feet_entry.grid(column=1, columnspan=3,row=3, sticky=(W, E))

ttk.Label(mainframe, text="内容:").grid( column=0,row=4, sticky=E)

t = Text(mainframe, width=70, height=40)
t.grid(column=1,columnspan=3,row=4, sticky=(W, E))

def send():
	try:
		proxy = xmlrpc.client.ServerProxy(url.get())
		script="proxy.{0}(title.get(),t.get(1.0,END),category.get(),englishname.get())".format(method.get());
		result = exec(script)
		messagebox.showinfo(message='发送成功')
	except Exception as inst:
		strg="发送失败:"+ str(inst)
		messagebox.showinfo(message=strg)
  
  
ttk.Button(mainframe, text="发送", command=send).grid(column=2, row=5, sticky=(W, E))

root.mainloop()