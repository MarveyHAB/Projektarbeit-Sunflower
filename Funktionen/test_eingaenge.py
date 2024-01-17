from machine import Pin
from time import sleep
SLEEP_PIN = Pin(4, Pin.OUT,value =0)
brake     = Pin(11 , Pin.OUT,value =0)
PSU24V    = Pin(12 , Pin.OUT, value=0)

ini_0geneigt   = Pin(16 , Pin.IN,Pin.PULL_UP)
test  = Pin(26 , Pin.IN,Pin.PULL_UP)

PSU_24V   = Pin (20, Pin.OUT,value =0)#24 aktivieren
led 			  = Pin('LED')

while True:
    led.value(1)
    sleep(0.1)
    if test.value() == 0:
        led.value(1)
    else:
        led.value(0)
    sleep(0.2)