import veml7700
import ds1307
from hmc5883l import HMC5883L
from sonne_jan import getAZ, getSEA
from drehen import step #sunPos
from machine import Pin, RTC, SoftI2C
from time import sleep, sleep_ms

btn_start         = Pin(22 , Pin.IN,PULL_DOWN)
btn_stopp         = Pin(26 , Pin.IN,PULL_DOWN)
btn_einfahren     = Pin(27 , Pin.IN,PULL_DOWN)
ini_ausgefaechert = Pin(21 , Pin.IN,PULL_DOWN)
anlage_ein = False

def ablauf(JackeWieHose):
    global anlage_ein
    anlage_ein = True
    while anlage_ein is True:
        AZ = getAZ(51,7,2)
        SE = getSEA(51,7,2)
        print("Sonnenrichtung:", AZ)
        print("Sonnenhöhe:" ,SE)
        
        if ini_ausgefaechert != 1:
            {
                #neigen 90grad
            #auffächern
            #drehen:
            step(int(AZ))
            #neigen auf Sonnenhöhe
            }
        else:
            step(int(AZ))
            #neigen auf Sonnenhöhe
        sleep(120)
        
def stopp(JackeWieHose):
    global anlage_ein
    anlage_ein = False

btn_start.irq(trigger=Pin.IRQ_FALLING, handler=ablauf)
btn_stopp.irq(trigger=Pin.IRQ_FALLING, handler=stopp)

