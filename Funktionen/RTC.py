from machine 	import Pin, I2C, RTC
from time 		import localtime, sleep
from sh1106 	import SH1106_I2C
import ds1307

i2c 		= I2C(0, scl=Pin(1), sda=Pin(0))
ds1307rtc 	= ds1307.DS1307(i2c, 0x68)
display		= SH1106_I2C(128, 64, i2c, Pin(28), 0x3c)

def sync_PC_time():
    zeit = localtime()
    ds1307rtc.disable_oscillator = False
    
    #Zeit von PC mit RTC Syncronisieren
    ds1307rtc.datetime = (zeit[0], zeit[1], zeit[2], zeit[3] , zeit[4], zeit[5], zeit[6], None)
    #Zeit von RTC auslesen
    dt = ds1307rtc.datetime
    #Pico Zeit setzen von RTC
    machine.RTC().datetime(ds1307rtc.datetimeRTC)
    
    display.sleep(False)
    display.fill(0)
    display.text('Sync PC '                          , 30, 20, 1)
    display.text('%02i.%02i.%i' %(zeit[2],zeit[1],zeit[0]) , 30, 30, 1)
    display.text('%02i:%02i'    %(zeit[3],zeit[4])            , 50, 40, 1)
    display.show()
    
def sync_RTC_Pico_time():
    RTC().datetime(ds1307rtc.datetimeRTC)
    zeit = localtime()
    
    display.sleep(False)
    display.fill(0)
    display.text('Sunflower '                              , 30, 20, 1)
    display.text('%02i.%02i.%i' %(zeit[2],zeit[1],zeit[0]) , 25, 30, 1)
    display.text('%02i:%02i'    %(zeit[3],zeit[4])            , 45, 40, 1)
    display.show()
    
    sleep(2)
