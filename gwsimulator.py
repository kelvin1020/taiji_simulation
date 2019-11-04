#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:洪卫
 
import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox as messagebox



class Application():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('太极引力波信号仿真')
        self.window.geometry('500x300')  # 这里的乘是小x 
        
        ############
        menubar = tk.Menu(self.window)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=filemenu)
        
        filemenu.add_command(label='New Template', command=self.sourceInConstruction)
        filemenu.add_command(label='Save Template', command=self.sourceInConstruction)
        filemenu.add_command(label='Open Template', command=self.sourceInConstruction)
        filemenu.add_separator()    # 添加一条分隔线
        filemenu.add_command(label='Exit', command=self.window.quit) # 用tkinter里面自带的quit()函数
        
        editmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Edit', menu=editmenu)
        editmenu.add_command(label='Cut', command=self.sourceInConstruction)
        editmenu.add_command(label='Copy', command=self.sourceInConstruction)
        editmenu.add_command(label='Paste', command=self.sourceInConstruction)
    
        submenu = tk.Menu(filemenu) # 和上面定义菜单一样，不过此处实在File上创建一个空的菜单
        filemenu.add_cascade(label='Import', menu=submenu, underline=0) # 给放入的菜单submenu命名为Import
    
        submenu.add_command(label='Submenu_1', command=self.sourceInConstruction)   # 这里和上面创建原理也一样，在Import菜单项中加入一个小菜单命令Submenu_1

        self.window.config(menu=menubar)
        self.sourceTemplateHello()
        self.window.mainloop()

    def sourceTemplateHello(self):
        self.windowTemplate = self.window
        self.selectFrame = tk.Frame(self.windowTemplate)
        self.selectFrame.pack(side='left')

        self.setFrame = tk.Frame(self.windowTemplate)
        self.setFrame.pack(side='right')

        #波源列表
        self.sourceVar = tk.StringVar(self.selectFrame)
        self.sourceVar.set(('EMRI','IMRI','SMBHB','Binary','Burst')) # 为变量设置值        

        self.sourceList = tk.Listbox(self.selectFrame, listvariable=self.sourceVar) 
        self.sourceList.pack()

        #显示已选
        self.printVar = tk.StringVar(self.selectFrame) 
        #确认按钮
        self.verify = tk.Button(self.selectFrame, text='确定', width=15, height=2, command=self.print_selection)
        self.verify.pack()
        #显示
        self.display = tk.Label(self.selectFrame, bg='green', fg='yellow',font=('Arial', 12), width=12, height=2,
            textvariable=self.printVar)
        self.display.pack()


        # window = sourceEMRIwindow()
        # name = self.nameInput.get() or 'world'

    def print_selection(self):
        try:
            value = self.sourceList.get(self.sourceList.curselection())   # 获取当前选中的文本
            self.printVar.set(value)  # 为label设置值
        except Exception as e:
            self.sourceSelectWarning()
        
 


    def sourceInConstruction(self):
        messagebox.showinfo(title='提示', message= '建设中...')

    def sourceSelectWarning(self):
        messagebox.showinfo(title='提示', message= '请选择波源')




if __name__ == "__main__":
    app = Application()





