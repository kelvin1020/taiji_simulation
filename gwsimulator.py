#!/usr/bin/env python
# coding: utf-8

# This is a software package to generate simulating waveform data for space-borne detectors. The data includes GW source, saterlite orbits, TDI noise and etc. All copyrights are credited to Han Wenbiao ....

# In[1]:


import sympy as sp #导入sympy包中的函数
import gravipy as gp #导入gravipy包的函数
import numpy as np  #导入numpy包的函数
import math
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint
import smtplib
import os
#import os.system
from decimal import *
from constant import *       # 导入常数表
from tkinter import *  # 导入图形界面


# Choose the type of gravitational wave souce one from EMRI, IMRI, SMBHB, GB, Burst

# In[2]:


from tkinter import ttk
class App:
    def __init__(self, master):
        self.master = master
        self.initWidgets()
    def initWidgets(self):
        # 创建Labelframe容器
        lf = ttk.Labelframe(self.master, text='请选择波源类型',
            padding=20)
        lf.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        sourcelist = ['EMRI','IMRI','SMBHB','Binary','Burst']
        i = 0
        self.intVar = IntVar()
        # 使用循环创建多个Radiobutton，并放入Labelframe中
        for source in sourcelist:
            Radiobutton(lf, text=source + '波源',
            value=i,
            variable=self.intVar).pack(side=LEFT)
            i += 1    
root = Tk()
root.title("太极引力波信号仿真界面")
# 改变窗口图标
root.iconbitmap('1.ico')
App(root)
root.mainloop()


# In[3]:


if sourcetype == 'EMRI' or sourcetype == 'IMRI':
    from EMRIparam import *  # 导入引力波源的物理参数


# In[ ]:


Distance = 1000*MPC # set source luminosity distance


# In[ ]:


sourcelist = ['EMRI','IMRI','SMBHB','Binary','Burst'] # GW source list
sourcetype = sourcelist[1] # choose one from the list
print(sourcelist)


# In[ ]:





# In[ ]:




