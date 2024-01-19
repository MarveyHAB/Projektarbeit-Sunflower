# kompass.py

# import webrepl_setup
# > d fuer disable
# Dann RST; Neustart!
#
import network; network.WLAN(network.AP_IF).active(False)
import gc
import sys, os
from machine import Pin, ADC, I2C
from time import sleep,ticks_ms
from math import atan2, degrees
import sh1106

import struct

class QMC5883L:
    QMC5883 = const(0x0D) # 7-Bit HWADR
    XRegL = const(0x00)
    XRegH = const(0x01)
    YRegL = const(0x02)
    YRegH = const(0x03)
    ZRegL = const(0x04)
    ZRegH = const(0x05)
    StatusReg = const(0x06)
    TempL = const(0x07)
    TempH = const(0x08)
    CtrlReg1 = const(0x09)
    CtrlReg2 = const(0x0A)
    Period = const(0x0B)
    
    DOR = const(0x04)
    OVL = const(0x02)
    DRDY= const(0x01)
    
    ModeMask= const(0xFC)
    Standby = const(0x00)
    Continuous = const(0x01)
    
    RateMask= const(0xF3)
    ORate10 = const(0x00)
    ORate50 = const(0x04)
    ORate100= const(0x08)
    ORate200= const(0x0C)
    
    ScaleMask=const(0xCF)
    FScale2 = const(0x00)
    FScale8 = const(0x10)
    
    OSRMask= const(0x3F)
    OSR512 = const(0x00)
    OSR256 = const(0x40)
    OSR128 = const(0x80)
    OSR64  = const(0xC0)
    
    SoftRST= const(0x80)
    RollOnt= const(0x40)
    IntEable=const(0x01)
    
    BezugsPegel = const(1000)
    
  
    def __init__(self,i2c,
                 ORate=ORate200,
                 FScale=FScale2,
                 OSR=OSR512,
                 ):
        self.i2c=i2c
        self.mode=Continuous
        self.oRate=ORate
        self.fScale=FScale
        self.osr=OSR
        self.configQMC()
        self.bezugsPegel=BezugsPegel
        self.readCalibration()        
        print("QMC5883L is @ {}".format(QMC5883))
        
    def writeToReg(self,reg,val):
        d=bytes([val & 0xFF])
        self.i2c.writeto_mem(QMC5883,reg,d)        

    def writeBytesToReg(self,reg,buf):
        self.i2c.writeto_mem(QMC5883,reg,buf)
    
    def configQMC(self):
        c1=self.mode | self.oRate | self.fScale | self.osr
        self.writeToReg(CtrlReg1,c1)
        c2=0
        self.writeToReg(CtrlReg2,c2)
        self.writeToReg(Period,0x01)
        

    def readNbytesFromReg(self,reg,n):
        return self.i2c.readfrom_mem(QMC5883,reg,n)

    def dataReady(self):
        val=self.i2c.readfrom_mem(QMC5883,StatusReg,1)[0]
        #print("status: {:08b}".format(val))
        drdy = val & DRDY
        ovl = (val & OVL)>>1
        return  drdy & (not ovl)# & (not dor)
    
    def readAxes(self):
        while not self.dataReady():
            pass
        achsen=self.readNbytesFromReg(0x00,6)
        x,y,z=struct.unpack("<hhh",achsen)
        return x,y,z

    def normalize(self,x,y):
        x-=k.xmid
        y-=k.ymid
        x=int(x/self.dx*1000+0.5)
        y=int(y/self.dy*1000+0.5)
        return x,y

    def axesAverage(self,n):
        xm,ym=0,0
        for i in range(n):
            x,y,z=k.readAxes()
            x,y=k.normalize(x,y)
            xm+=x
            ym+=y
        xm=int(xm/n)
        ym=int(ym/n)
        return x,y

    def calcAngle(self,x,y):
        angle=0
        if abs(y) < 1:
            if x > 0:
                angle = 0
            if x < 0:
                angle = 180
        else: # y > 1
            if abs(x) < 1:
                if y > 0:
                    angle = 90
                if y < 0:
                    angle = 270
            else: # x > 1
                angle = degrees(atan2(y,x))
                if angle < 0:
                    angle+=360
        return angle
    
    def readTemperature(self):
        return (struct.unpack("<h",\
                k.readNbytesFromReg(7,2))[0]+4000)/100
    
    def calibrate(self):
        xmin=32000
        xmax=-32000
        ymin=32000
        ymax=-32000
        finished=self.TimeOut(20000)
        print("CALIBRATING")
        print("ROTATE DEVICE")
        sleep(3)
        while not finished():
            x,y,z=self.readAxes()
            xmin=(xmin if x >= xmin else x)
            xmax=(xmax if x <= xmax else x)
            ymin=(ymin if y >= ymin else y)
            ymax=(ymax if y <= ymax else y)
        self.xmid=(xmin+xmax)//2
        self.ymid=(ymin+ymax)//2
        print (xmin,self.xmid, xmax)
        print (ymin,self.ymid, ymax)
        self.dx=(xmax-xmin)//2
        self.dy=(ymax-ymin)//2
        print (self.dx, self.dy)
        with open("config.txt","w") as f:
            f.write(str(self.xmid)+"\n")
            f.write(str(self.ymid)+"\n")
            f.write(str(self.dx)+"\n")
            f.write(str(self.dy)+"\n")
        print("CAL. DONE")
        
    def readCalibration(self):
        try:
            with open("config.txt","r") as f:
                self.xmid=int(f.readline())
                self.ymid=int(f.readline())
                self.dx=int(f.readline())
                self.dy=int(f.readline())
        except OSError:
            self.calibrate()
    
    def TimeOut(self,t):
        start=ticks_ms()
        def compare():
            return int(ticks_ms()-start) >= t
        return compare   


# **********************************************************
def alleAus(show=True):
    for i in range(neoCnt):
        np[i]=(0,0,0)
    if show:
        np.write()

brake = 		Pin(11,Pin.OUT,value =1)
 
delta=22.5 #keine ahnung
h=ADC(0)   #keine ahnung
i2c=I2C(0, scl=Pin(1), sda=Pin(0))
i2c.writeto(0x70, b'\x02')
sleep(.5)
k=QMC5883L(i2c,OSR=OSR512,ORate=ORate200,FScale=FScale2) #Kompass
i2c.writeto(0x70, b'\x03')
sleep(0.1)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c) #Display

taste=Pin(2,Pin.IN,Pin.PULL_UP)

if taste.value()==0:
    k.calibrate()
else:
    while 1:
        i2c.writeto(0x70, b'\x02')
        a=k.axesAverage(100)
        w=int(k.calcAngle(a[0],a[1]))
        print(w)
        strWinkel = str(w)
        i2c.writeto(0x70, b'\x03')
        display.fill(0)
        display.text(strWinkel, 0, 0, 1)
        display.show()
        #print(str(int(w+0.5)))