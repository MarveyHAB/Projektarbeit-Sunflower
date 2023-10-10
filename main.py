import veml7700
import ds1307
from hmc5883l import HMC5883L
from sonne_jan import getAZ, getSEA
from drehen import step #sunPos
from machine import Pin, RTC, SoftI2C, Timer
from time import sleep, sleep_ms

#Timer
ausrichtung_check = Timer()

#BTN
btn_startstopp    = Pin(22 , Pin.IN,Pin.PULL_DOWN)
btn_NOTStopp      = Pin(26 , Pin.IN,Pin.PULL_DOWN)
btn_einfahren     = Pin(27 , Pin.IN,Pin.PULL_DOWN)
ini_ausgefaechert = Pin(21 , Pin.IN,Pin.PULL_DOWN)
anlage_ein        = False

def ISR_ausrichtung(abc):
    #Sonnenstand aktualisieren
    #Positionen checken ggf. neu verfahren
    

def ablauf(pin22):
    global anlage_ein
    anlage_ein = not anlage_ein
    if(anlage_ein == True):
        ausrichtung_check.init(period=120000 , mode=Timer.PERIODIC, callback=ISR_ausrichtung)
    else
        ausrichtung_check.deinit()
        
    while anlage_ein is True:
        if ini_ausgefaechert != 1:
            {
                #neigen 90grad
            #auffächern
            #drehen:
            step(int(AZ))
            #neigen auf Sonnenhöhe
            }
        else:
            step(int(AZ))#
            
            #neigen auf Sonnenhöhe
        sleep(120)
    ausrichtung_check.deinit()
    
def NOTStopp(pin26):
    global anlage_ein
    anlage_ein = False
    ausrichtung_check.deinit()

btn_startstopp.irq(trigger=Pin.IRQ_FALLING, handler=ablauf)
btn_NOTStopp.irq(trigger=Pin.IRQ_FALLING, handler=NOTStopp)

