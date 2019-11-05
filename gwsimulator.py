#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:洪卫
 
import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox as messagebox

####teukolsky
from lib.waveform import teukolsky
from astropy import constants as const #import constants 
import astropy.units as u              #import unit
import numpy as np  #import numpy, and name it as np
from lib.waveform import get_td_waveform
import pandas as pd

# Constants
G = (const.G).value # gravitational constant
C = (const.c).value # the speed of light


def WaveDataOut(**kwargs):
    #   Parameters
    duration = 2.0**16.0         #信号持续时间(duration of signal) 2^16, 0.75d, 2^25 ,1.06yr
    step = 4

    atilde = np.sqrt(kwargs['SpinxBH']**2 + kwargs['SpinyBH']**2 + kwargs['SpinzBH']**2)  # 自旋参量
    nu = kwargs['MassCO'] / kwargs['MassBH'] # 质量比? 对称质量比
    M = ((kwargs['MassBH'] + kwargs['MassCO']) * const.M_sun).to(u.kg).value  #the mass of system, kilogram
    # m = (1e1 * const.M_sun).to(u.kg).value  #the mass of small compact body, kilogram

    l = np.arange(2,3)      
    # m = 2
    k = np.arange(-2,12,1)                   #the nth harmonic

    ########################
    R_unit = (G * M / C**2)#                #the unit length in G = C = 1 system, metre
    # t_unit = R_unit / C    #                #the unit time in G = C = 1 system, second
    ########################

    e = kwargs['ECC']                                 #eccentricity of orbit
    p = kwargs['PM']  * R_unit                         #semi-latus rectum

    a = p / (1 - e**2)                      #the semi-major axis of orbit, metre

    D = (1.00 * u.Gpc).to('m').value

    wave = teukolsky(atilde = atilde, nu = nu, M = M, l = l, k = k, e = e, a = a, D = D)
    wave.ecalculate(duration = duration, delta_t = step)
    hp, hc = get_td_waveform(template=wave)

    timeVec = (np.array(hp.sample_times)).reshape(-1, 1)
    hpVec =  (np.array(hp)).reshape(-1, 1)
    hcVec =  (np.array(hc)).reshape(-1, 1)
    waveMat = np.concatenate((timeVec, hpVec, hcVec), axis = 1)
    waveData = pd.DataFrame(waveMat, columns = ['timeSecond', 'hp', 'hc'])
    waveData.to_csv('waveDataEMRI.dat')# columns=['JDTimeTCB']  #导出csv文件
    return waveData


class Application():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('空间引力波信号仿真')
        self.window.geometry('350x200')  # 这里的乘是小x 
        
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

        helpmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=helpmenu)
        helpmenu.add_command(label='About', command=self.aboutInformation)

        self.window.config(menu=menubar)
        self.sourceTemplateHello()
        self.window.mainloop()

    def sourceTemplateHello(self):
        self.windowTemplate = self.window

        #波源列表
        self.sourceVar = tk.StringVar(self.windowTemplate)
        self.sourceVar.set(('EMRI','IMRI','SMBHB','Binary','Burst')) # 为变量设置值        
        self.sourceList = tk.Listbox(self.windowTemplate, listvariable=self.sourceVar, width=10, height=5) 
        self.sourceList.place(x=20, y=30, anchor='nw')
        #显示已选
        self.printVar = tk.StringVar(self.windowTemplate) 
        #确认按钮
        self.verify = tk.Button(self.windowTemplate, text='确定', width=10, height=2, command= self.print_selection)
        self.verify.place(x=20, y=125, anchor='nw')
  

        #显示
        tk.Label(self.windowTemplate, text='Source Type',font=('Arial', 12), width=12, height=2).place(x=200, y=10, anchor='nw')

        self.display = tk.Label(self.windowTemplate, bg='green', fg='yellow',font=('Arial', 12), width=12, height=1,
            textvariable=self.printVar)
        self.display.place(x=200, y=35, anchor='nw')

        self.coeffSet0 = tk.Button(self.windowTemplate, text='参数设定', width=10, height=2, command=self.sourceSelectWarning)
        self.coeffSet0.place(x=200, y=55, anchor='nw') # 占据位置


    def sourceEMRIset(self):
            self.windowTemplateEMRI = tk.Toplevel(self.window)
            self.windowTemplateEMRI.title('EMRI参数设定')
            self.windowTemplateEMRI.geometry('700x450')  # 这里的乘是小x 

            self.isWaveOK = tk.StringVar(self.windowTemplateEMRI) 
            self.isWaveOK.set('设定参数') 

            #波形参数
            self.varMassBH = tk.StringVar(self.windowTemplateEMRI) 
            self.varSpinxBH = tk.StringVar(self.windowTemplateEMRI) 
            self.varSpinyBH = tk.StringVar(self.windowTemplateEMRI) 
            self.varSpinzBH = tk.StringVar(self.windowTemplateEMRI) 
            self.varMassCO  = tk.StringVar(self.windowTemplateEMRI) 
            self.varSpinxCO = tk.StringVar(self.windowTemplateEMRI) 
            self.varSpinyCO = tk.StringVar(self.windowTemplateEMRI) 
            self.varSpinzCO  = tk.StringVar(self.windowTemplateEMRI)            
            self.varECC = tk.StringVar(self.windowTemplateEMRI) 
            self.varPM  = tk.StringVar(self.windowTemplateEMRI) 
            self.varIOTA = tk.StringVar(self.windowTemplateEMRI) 

            #默认值
            self.varMassBH.set('1e6') 
            self.varSpinxBH.set('0') 
            self.varSpinyBH.set('0') 
            self.varSpinzBH.set('0.5') 
            self.varMassCO.set('1e2') 
            self.varSpinxCO.set('0') 
            self.varSpinyCO.set('0')
            self.varSpinzCO.set('0')          
            self.varECC.set('0.5')
            self.varPM.set('8.0')
            self.varIOTA.set('0.25')

            tk.Label(self.windowTemplateEMRI, text='MassBH (Mass_Sun)',font=('Arial', 10)).grid(row=1, column=1, padx=10, pady=10, ipadx=10, ipady=10)
            self.InputMassBH = tk.Entry(self.windowTemplateEMRI, textvariable=self.varMassBH, show=None, font=('Arial', 12), width=12)  # 显示成明文形式
            self.InputMassBH.grid(row=1, column=2, padx=10, pady=10, ipadx=10, ipady=10)
       
            tk.Label(self.windowTemplateEMRI, text='SpinxBH',font=('Arial', 14)).grid(row=2, column=1, padx=10, pady=10, ipadx=10, ipady=10)
            self.InputSpinxBH = tk.Entry(self.windowTemplateEMRI, textvariable=self.varSpinxBH, show=None, font=('Arial', 12), width=12)  # 显示成明文形式
            self.InputSpinxBH.grid(row=2, column=2, padx=10, pady=10, ipadx=10, ipady=10)

            tk.Label(self.windowTemplateEMRI, text='SpinyBH',font=('Arial', 14)).grid(row=3, column=1, padx=10, pady=10, ipadx=10, ipady=10)
            self.InputSpinyBH = tk.Entry(self.windowTemplateEMRI, textvariable=self.varSpinyBH, show=None, font=('Arial', 12), width=12)  # 显示成明文形式
            self.InputSpinyBH.grid(row=3, column=2, padx=10, pady=10, ipadx=10, ipady=10)

            tk.Label(self.windowTemplateEMRI, text='SpinzBH',font=('Arial', 14)).grid(row=4, column=1, padx=10, pady=10, ipadx=10, ipady=10)
            self.InputSpinzBH = tk.Entry(self.windowTemplateEMRI, textvariable=self.varSpinzBH, show=None, font=('Arial', 12), width=12)  # 显示成明文形式
            self.InputSpinzBH.grid(row=4, column=2, padx=10, pady=10, ipadx=10, ipady=10)

            tk.Label(self.windowTemplateEMRI, text='MassCO (Mass_Sun)',font=('Arial', 10)).grid(row=1, column=3, padx=10, pady=10, ipadx=10, ipady=10)
            self.InputMassCO = tk.Entry(self.windowTemplateEMRI, textvariable=self.varMassCO, show=None, font=('Arial', 12), width=12)  # 显示成明文形式
            self.InputMassCO.grid(row=1, column=4, padx=10, pady=10, ipadx=10, ipady=10)

            tk.Label(self.windowTemplateEMRI, text='SpinxCO',font=('Arial', 14)).grid(row=2, column=3, padx=10, pady=10, ipadx=10, ipady=10)
            self.InputSpinxCO = tk.Entry(self.windowTemplateEMRI, textvariable=self.varSpinxCO, show=None, font=('Arial', 12), width=12)  # 显示成明文形式
            self.InputSpinxCO.grid(row=2, column=4, padx=10, pady=10, ipadx=10, ipady=10)

            tk.Label(self.windowTemplateEMRI, text='SpinyCO',font=('Arial', 14)).grid(row=3, column=3, padx=10, pady=10, ipadx=10, ipady=10)
            self.InputSpinyCO = tk.Entry(self.windowTemplateEMRI, textvariable=self.varSpinyCO, show=None, font=('Arial', 12), width=12)  # 显示成明文形式
            self.InputSpinyCO.grid(row=3, column=4, padx=10, pady=10, ipadx=10, ipady=10)

            tk.Label(self.windowTemplateEMRI, text='SpinzCO',font=('Arial', 14)).grid(row=4, column=3, padx=10, pady=10, ipadx=10, ipady=10)
            self.InputSpinzCO = tk.Entry(self.windowTemplateEMRI, textvariable=self.varSpinzCO, show=None, font=('Arial', 12), width=12)  # 显示成明文形式
            self.InputSpinzCO.grid(row=4, column=4, padx=10, pady=10, ipadx=10, ipady=10)

            tk.Label(self.windowTemplateEMRI, text='ECC',font=('Arial', 14)).grid(row=5, column=1, padx=10, pady=10, ipadx=10, ipady=10)
            self.InputECC = tk.Entry(self.windowTemplateEMRI, textvariable=self.varECC, show=None, font=('Arial', 12), width=12)  # 显示成明文形式
            self.InputECC.grid(row=5, column=2, padx=10, pady=10, ipadx=10, ipady=10)

            tk.Label(self.windowTemplateEMRI, text='PM (M)',font=('Arial', 14)).grid(row=6, column=1, padx=10, pady=10, ipadx=10, ipady=10) 
            self.InputPM = tk.Entry(self.windowTemplateEMRI, textvariable=self.varPM, show=None, font=('Arial', 12), width=12)  # 显示成明文形式
            self.InputPM .grid(row=6, column=2, padx=10, pady=10, ipadx=10, ipady=10)

            tk.Label(self.windowTemplateEMRI, text='IOTA (PI)',font=('Arial', 14)).grid(row=7, column=1, padx=10, pady=10, ipadx=10, ipady=10)
            self.InputIOTA = tk.Entry(self.windowTemplateEMRI, textvariable=self.varIOTA, show=None, font=('Arial', 12), width=12)  # 显示成明文形式
            self.InputIOTA.grid(row=7, column=2, padx=10, pady=10, ipadx=10, ipady=10)

            #生成波形按钮 
            self.coeffOK = tk.Button(self.windowTemplateEMRI, text='生成波形', width=10, height=2,\
                command=self.waveform_making,state=tk.NORMAL)
            self.coeffOK.grid(row=6, column=3, padx=10, pady=10, ipadx=10, ipady=10)
            self.coeffOK.bind("<Button-1>", self.waveStatus)
            
            #状态显示
            self.displayWaveStatus = tk.Label(self.windowTemplateEMRI, bg='green', fg='yellow',font=('Arial', 10), width=10, height=2,
                textvariable=self.isWaveOK)
            self.displayWaveStatus.grid(row=6, column=4, padx=10, pady=10, ipadx=10, ipady=10)

            #绘图按钮
            #self.plotWave = tk.Button(self.windowTemplateEMRI, text='参数设定', width=10, height=2, command=self.sourceSelectWarning)
            #self.plotWave.grid(row=7, column=3, padx=10, pady=10, ipadx=10, ipady=10) # 占据位置

    #波形生成
    def waveStatus(self, event):
        try:
            self.isWaveOK.set('波形生成中') 

        except Exception as e:
            self.warningInformation(e)



    def waveform_making(self):
        try:
            MassBH = float(self.varMassBH.get()) 
            SpinxBH = float(self.varSpinxBH.get()) 
            SpinyBH = float(self.varSpinyBH.get()) 
            SpinzBH = float(self.varSpinzBH.get()) 
            MassCO  = float(self.varMassCO.get())
            SpinxCO = float(self.varSpinxCO.get()) 
            SpinyCO = float(self.varSpinyCO.get())
            SpinzCO = float(self.varSpinzCO.get())         
            ECC = float(self.varECC.get())
            PM = float(self.varPM.get())
            IOTA = float(self.varIOTA.get())

            with open('./coeff.dat','w') as f:
                print(MassBH, SpinxBH, SpinyBH, SpinzBH, MassCO, SpinxCO, SpinyCO, SpinzCO, ECC, PM, IOTA, file=f)

            kwargs = dict(MassBH=MassBH, SpinxBH=SpinxBH, SpinyBH=SpinyBH, SpinzBH=SpinzBH, \
                MassCO=MassCO, SpinxCO=SpinxCO, SpinyCO=SpinyCO, SpinzCO=SpinzCO, ECC=ECC, PM=PM, IOTA=IOTA)

            #生成波形
            WaveDataOut(**kwargs)
            
            self.isWaveOK.set('波形已生成') 
             

        except Exception as e:
            self.warningInformation(e)
  


    def print_selection(self):
        try:
            self.selectValue = self.sourceList.get(self.sourceList.curselection())   # 获取当前选中的文本
            self.printVar.set(self.selectValue)  # 为label设置值

            #确认按钮
            self.commandDict = {'EMRI' : self.sourceEMRIset,
                       'IMRI' : self.sourceInConstruction,
                      'SMBHB' : self.sourceInConstruction,
                     'Binary' : self.sourceInConstruction,
                      'Burst' : self.sourceInConstruction}

            self.inputCommand = self.commandDict.get(self.selectValue)
            self.coeffSet = tk.Button(self.windowTemplate, text='参数设定', width=10, height=2, command=self.inputCommand)
            self.coeffSet.place(x=200, y=55, anchor='nw') # 覆盖原有按钮
        except Exception:
            self.sourceSelectWarning()
        

    def sourceInConstruction(self):
        messagebox.showinfo(title='提示', message= '建设中...')

    def sourceSelectWarning(self):
        messagebox.showinfo(title='提示', message= '请选择波源')

    def warningInformation(self, e):
        messagebox.showinfo(title='警告', \
            message= e)

    def aboutInformation(self):
        messagebox.showinfo(title='空间引力波探测器仿真', \
            message= '空间引力波探测器仿真\n\n中国科学院上海天文台\n引力波与相对论基本天文学课题组\n\n版权所有\n\n')

if __name__ == "__main__":
    app = Application()





