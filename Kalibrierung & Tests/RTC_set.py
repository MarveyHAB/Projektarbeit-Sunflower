from machine import Pin, I2C, RTC
from time import localtime
# from machine import Pin, I2C
import ds1307
import time

zeit = localtime()

# full test code
i2c 	= I2C(0, scl=Pin(1), sda=Pin(0))
#i2c0 = SoftI2C(scl=Pin(1), sda=Pin(0))
ds1307rtc = ds1307.DS1307(i2c, 0x68)

#print(dir(ds1307rtc))

# set and read disable_osclator property 
ds1307rtc.disable_oscillator = True
print("disable_oscillator  = ", ds1307rtc.disable_oscillator)
ds1307rtc.disable_oscillator = False
print("disable_oscillator = ", ds1307rtc.disable_oscillator,"\n")

print("date time and weekday from DS1307")
print(ds1307rtc.datetime,"\n")

# set time (year, month, day, hours. minutes, seconds, weekday: integer: 0-6 )
zeit = localtime()
ds1307rtc.datetime = (zeit[0], zeit[1], zeit[2], zeit[3] , zeit[4], zeit[5], zeit[6], None)

# read time
dt = ds1307rtc.datetime
print(dt)

# wait 3.9 seconds and read time again
time.sleep(3.9) 
print(ds1307rtc.datetime,"\n")

#read time in format suitable to set the
print("date time from DS1307 in format needed to set pico RTC clock") 
print(ds1307rtc.datetimeRTC,"\n")

print("time from pico internal RTC")
print(time.localtime(),"\n")

print("set pico clock from DS1307 and print time from internal pico clock") 
machine.RTC().datetime(ds1307rtc.datetimeRTC)
print(time.localtime())
