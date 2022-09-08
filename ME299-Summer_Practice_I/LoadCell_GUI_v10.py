"""
Load Cell calibration, data acquisition, storing and visualization tool from
Arduino serial port.

Components: Load cell, HX711 signal amplifier, DHT22, BMP180, I2C LCD screen and 2xbuttons

Calibration is done through linear regression. Check the relevant document and the video.
This setup was created to serve as an introduction to mass metrology to students.

Note 1: This code is independent of the DHT22 and BMP180. The data for those are 
displayed a LCD screen although it would be more practical to read those from serial aswell.

Note 2: The setup works reasonably well, but there is a slight drifting error on the load cell.
"Tare" button was added to remedy this issue.
"""

from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import scipy
from scipy import stats

import serial
import time
import matplotlib.pyplot as plt
import random as rn
import sys

from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

class MyWindow:
    def __init__(self, win):
        self.port = "COM3"
        self.baud = 9600
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow()
        
        self.p = self.win.addPlot(title="Load Cell Readings")
        self.p.setLabel('left', "<span style=\"color:green;font-size:20px\">Mass (g)</span>")
        self.p.setLabel('bottom', "<span style=\"color:green;font-size:20px\">Time (s)</span>")
        self.p.setTitle("Load Cell Readings", color="g", size="15pt")
        self.p.showGrid(x=True, y=True)
        self.curve = self.p.plot(pen={'color':'g'})

        self.windowWidth = 500
        self.Xm = linspace(0,0,self.windowWidth)
        self.Ym = linspace(0,0,self.windowWidth)

        self.t_count=0
        self.button1=1
        self.cal_fac=1000
        self.off=0
        self.rec=0
        self.t_rec=[]
        self.m_rec=[]
        self.sesh=1
        
        image1 = Image.open("port.png")
        photo1 = ImageTk.PhotoImage(image1)

        image2 = Image.open("set1.png")
        photo2 = ImageTk.PhotoImage(image2)

        image3 = Image.open("save.png")
        photo3 = ImageTk.PhotoImage(image3)

        image4 = Image.open("cal3.png")
        photo4 = ImageTk.PhotoImage(image4)

        self.ico1 = Label(win, image=photo1)
        self.ico1.image = photo1
        self.ico1.place(x=20, y=10)

        self.ico2 = Label(win, image=photo2)
        self.ico2.image = photo2
        self.ico2.place(x=20, y=120)

        self.ico3 = Label(win, image=photo3)
        self.ico3.image = photo3
        self.ico3.place(x=25, y=270)

        self.ico4 = Label(win, image=photo4)
        self.ico4.image = photo4
        self.ico4.place(x=20, y=400)

        self.scrollbar = Scrollbar(win) 
        self.scrollbar.pack( side = RIGHT, fill = Y ) 
        self.List1 = Listbox(win, yscrollcommand = self.scrollbar.set, width=60, height=29)
        self.List1.place(x=420, y=30) 
        self.List1.insert(END, " "*32+ "...INITIATING THE PROGRAM..." + '\n')
        self.scrollbar.config( command = self.List1.yview )

        self.L1=Label(win, text='Arduino Port:'+'\n'+"(e.g. COM1)")
        self.L2=Label(win, text='Calibration Factor:'+'\n'+"(Default = 1000)")
        self.L3=Label(win, text='Offset Value:'+'\n'+"(Default = 0)")
        self.e1 = Entry(win) 
        self.e2 = Entry(win) 
        self.e3 = Entry(win)
        self.e1.place(x=230, y=30)
        self.e2.place(x=230, y=130)
        self.e3.place(x=230, y=180)
        self.L1.place(x=145, y=30)
        self.L2.place(x=120, y=130)
        self.L3.place(x=150, y=180)

        self.L4=Label(win, text='Do you want to record the readings?')
        self.L4.place(x=150,y=270)
        v0=IntVar()
        v0.set(1)
        self.r1=Radiobutton(win, text="Yes", variable=v0,value=1, command=self.yes)
        self.r2=Radiobutton(win, text="No", variable=v0,value=2, command=self.no)
        self.r1.place(x=180,y=300)
        self.r2.place(x=260, y=300)

        self.L5=Label(win, text='Enter measurement data below to obtain'+'\n'
                 +'linear regression corrected settings.'+'\n'+
                 '(Data format: 0, 100, 200, 300, etc.)')
        self.L5.place(x=150, y=400)
        self.L6=Label(win, text='Known Values:')
        self.L6.place(x=115, y=470)
        self.L7=Label(win, text='Measured Values:')
        self.L7.place(x=100, y=500)
        self.e4 = Entry(win) 
        self.e5 = Entry(win)
        self.e4.place(x=200, y=470)
        self.e5.place(x=200, y=500)
        self.bt1 = Button(win, text = 'Calculate', fg ='blue', command=self.linreg)
        self.bt1.place(x=230, y=530)

        self.bt2 = Button(win, text = 'Begin', fg ='green', width=17, command=self.begin)
        self.bt2.place(x=520, y=530)

    def linreg(self):
        KL=(str(self.e4.get())).split(",")
        z=0
        for z in range(len(KL)):
            KL[z]=float(KL[z])
        ML=(str(self.e5.get())).split(",")
        z=0
        for z in range(len(ML)):
            ML[z]=float(ML[z])
        
        if len(ML)!=len(KL):
            self.List1.insert(END, "Two data sets have unequal quantities of data.")
        else:
            m1, c1, r1, p1, std1 =scipy.stats.linregress(KL, ML)
            self.List1.insert(END, '\n',"Linear regression calibration factor: ", (1/m1)*1000)
            self.List1.insert(END, "Linear regression offset value: ", -c1)
            self.List1.insert(END, "R^2 value of the linear fit: ", r1**2, '\n')

    def begin(self):
        self.List1.insert(END, "" + '\n')
        self.List1.insert(END, '\n'+"Beginning session: " +str(self.sesh)+ '\n'+'\n')
        self.List1.insert(END, "" + '\n')
        if self.sesh ==1:
            if self.e1.get()!="":
                self.port=str(self.e1.get())
        
            if self.e2.get()!="" or self.e3.get()!="":   
                self.cal_fac=float(self.e2.get())
                self.pff=float(self.e3.get())
            self.ser = serial.Serial(self.port, self.baud, timeout=4)
        
        time.sleep(3)
        while self.button1 != 0:
            self.update()
        self.save()
        pg.QtGui.QApplication.exec_()
        self.reset()

    def update(self):  
        t1=time.perf_counter()
        self.Xm[:-1] = self.Xm[1:]
        self.Ym[:-1] = self.Ym[1:]
        value1 = str(self.ser.readline())
        value2 = value1.split("'")
        value3 = value2[1].split(" ")
        value4 = value3[0]
        self.button1 = int(value3[2])
        button2=int(value3[4].split("\\r\\n")[0])
        if isfloat(value4):
            result = ((float(value4)/1000)*self.cal_fac+self.off)
            if button2 ==0:
                self.off=((float(value4)/1000)*self.cal_fac)*(-1)
            t=time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            self.t_rec.append(current_time)
            self.m_rec.append(float(result))
            
            self.Xm[-1] = float(result)
            self.Ym[-1] = self.t_count
            self.curve.setData(self.Ym, self.Xm)
            self.p.setRange(xRange=[max(0, self.t_count-30), self.t_count])
            self.p.setLabel('top', "Current: "+str(float(result))+"g")
            self.List1.insert(END, str(current_time)+"  Reading: "+str(result)+"g")  
            QtGui.QApplication.processEvents()
        t2=time.perf_counter()
        t_int=t2-t1
        self.t_count+=t_int
    
    def yes(self):
        self.rec=1
    def no(self):
        self.rec=0
    
    def save(self):
        if self.rec==1:
            filename="Mass Measurement Data "+str(rn.randint(0, 999999999))
            record_file=open(filename, "w")
            i=0
            record_file.write("  Time      Mass (g)"+'\n')
            for i in range(len(self.t_rec)):
                record_file.write(self.t_rec[i]+"      "+str(self.m_rec[i])+'\n')
            record_file.close()
    
    def reset(self):
        self.t_count=0
        self.button1=1
        self.t_rec=[]
        self.m_rec=[]
        self.sesh+=1
        self.Xm = linspace(0,0,self.windowWidth)
        self.Ym = linspace(0,0,self.windowWidth)

window=Tk()
mywin=MyWindow(window)
window.title('Load Cell GUI V2')
window.geometry("800x600+10+10")
window.mainloop()