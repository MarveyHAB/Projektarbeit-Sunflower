# kompass_test.py

# import webrepl_setup
# > d fuer disable
# Dann RST; Neustart!
import network; network.WLAN(network.AP_IF).active(False)
#
import sys, os
from machine import Pin, ADC, SoftI2C
from time import sleep,ticks_ms
from neopixel import NeoPixel
from oled import OLED
from math import atan2, degrees

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
    AutoInc = const(0x40)
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
        self.i2c=i2c
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
        c2=0x00
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
        d.clearAll()
        d.writeAt("CALIBRATING",0,0,False)
        d.writeAt("ROTATE DEVICE",0,1)
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
        self.xFaktor=BezugsPegel/self.dx
        self.yFaktor=BezugsPegel/self.dy
        with open("config.txt","w") as f:
            f.write(str(self.xmid)+"\n")
            f.write(str(self.ymid)+"\n")
            f.write(str(self.dx)+"\n")
            f.write(str(self.dy)+"\n")
            f.write(str(self.xFaktor)+"\n")
            f.write(str(self.yFaktor)+"\n")
        d.writeAt("CAL. DONE",0,2)
        
    def readCalibration(self):
        try:
            with open("config.txt","r") as f:
                self.xmid=int(f.readline())
                self.ymid=int(f.readline())
                self.dx=int(f.readline())
                self.dy=int(f.readline())
                self.xFaktor=float(f.readline())
                self.yFaktor=float(f.readline())
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
        
def nord(alpha,n):  # Winkel vom QMC5883, Anzahl LEDs
    alleAus(False)
    beta=360-alpha  # Nord-Winkel
    step=360//n     # Winkelschritt
    hstep=step//2
    q=(beta//step)%n    # Hauptrichtung LED
    m=beta%step     # Zwischenwert LED
    hF=(1023-h.read())/1023
    print(q,m," --- ", led[q])
    if 1 < m < step//2: # naeher an q
        np[led[q]]=(int(255*hF),0,0) # q leuchtet voll
        np[led[(q+1)%n]]=(0,0,int(64*(m)/hstep*hF)) 
        np[(led[q]+6)%n]=(0,int(64*hF),0) # q+6 leuchtet voll
        np[(led[(q+1)%n]+6)%n]=(0,0,int(64*(m)/hstep*hF))
    elif m > step//2: # naeher an q+1
        np[led[(q+1)%n]]=(int(hF*255),0,0) # q+1 leuchtet voll
        np[led[q]]=(0,0,int(64*(step-m)/hstep*hF)) # prop. Helligkeit
        np[(led[(q+1)%n]+6)%n]=(0,int(hF*64),0) # q+1+6 leuchtet voll
        np[(led[q]+6)%n]=(0,0,int(64*(step-m)/hstep*hF)) # prop. Helligkeit
    elif m == step//2:
        np[led[q]]=(int(255*hF),0,0)
        np[led[(q+1)%n]]=(int(255*hF),0,0)
        np[(led[(q+1)%n]+6)%n]=(0,int(hF*64),0)
        np[(led[q]+6)%n]=(0,int(hF*64),0)
    else:
        np[led[q]]=(int(255*hF),0,0)
        np[(led[q]+6)%n]=(0,int(hF*64),0)
    np.write()
 
chip=sys.platform
if chip == 'esp8266':
    # Pintranslator fuer ESP8266-Boards
    # LUA-Pins     D0 D1 D2 D3 D4 D5 D6 D7 D8
    # ESP8266 Pins 16  5  4  0  2 14 12 13 15 
    #                 SC SD
    SCL=Pin(5) # S01: 0
    SDA=Pin(4) # S01: 2
elif chip == 'esp32':
    SCL=Pin(21)
    SDA=Pin(22)
else:
    raise OSError ("Unbekannter Port")

neoPin=Pin(14,Pin.OUT,value=1)
neoCnt=12
np=NeoPixel(neoPin,neoCnt)
# led=[6,7,8,9,10,11,0,1,2,3,4,5]
led=[3,4,5,6,7,8,9,10,11,0,1,2]
h=ADC(0)
i2c=SoftI2C(SCL,SDA,freq=400000)
d=OLED(i2c)
k=QMC5883L(i2c,OSR=OSR512,ORate=ORate200,FScale=FScale2)

taste=Pin(0,Pin.IN,Pin.PULL_UP)

if taste.value()==0:
    k.calibrate()
else:
    pass