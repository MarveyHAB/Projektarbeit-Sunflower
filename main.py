import veml7700
import ds1307
from hmc5883l import HMC5883L
from sonne_jan import getAZ, getSEA
from drehen import drehen_grundpos, drehen_sonne
from neigen import neigen0, neigen90, neigen_sonne
from faechern import auffaechern, einfaechern
from machine import Pin, RTC, SoftI2C, Timer
from time import sleep, sleep_ms

#Timer
ausrichtung_check = Timer()

#BTN
btn_startstopp    	= Pin(27 , Pin.IN,Pin.PULL_UP)
btn_NOTStopp      	= Pin(26 , Pin.IN,Pin.PULL_UP)
#btn_einfahren     	= Pin(22 , Pin.IN,Pin.PULL_UP)
ini_ausgefaechert 	= Pin(21 , Pin.IN,Pin.PULL_UP)
anlage_ein        	= False
fehler				= False

def ISR_ausrichtung(abc):
    drehen_sonne()
    neigen_sonne()

def ablauf(pin22):
    global anlage_ein, fehler
    anlage_ein = not anlage_ein
    
    if(anlage_ein == True and fehler == 0):
        if fehler == 0:
            if neigen90() == 0:
                Print("Timeout! Endlage neigen konnte nicht errreicht werden!")
                anlage_ein = False
        if fehler == 0:
            if auffaechern() == 0:
                Print("Timeout! Endlage Auffächern konnte nicht errreicht werden!")
                anlage_ein = False
        if fehler == 0:
            if drehen_sonne == Fasle:
                Print("Timeout! Endlage Drehen konnte nicht errreicht werden!")
                anlage_ein = False
        if fehler == 0:
            if neigen_sonne() == 0:
                Print("Timeout! Endlage Neigen konnte nicht errreicht werden!")
                anlage_ein = False
        if fehler == 0:
            ausrichtung_check.init(period=120000 , mode=Timer.PERIODIC, callback=ISR_ausrichtung) #TODO Zeit!
            
    elif fehler == 0: 
        #Was soll passieren wenn fehler True????????
        ausrichtung_check.deinit()
        neigen90()
        drehen_grundpos()
        einfaechern()
        neigen0()
        
    if Fehler == True:
        #11 = Fehler aufneigen,  12 = Fehler zuneigen        
        #21 = Fehler auffächern, 22 = Fehler zufächern
        #31 = Fehler drehen
        #41 = NOTHALT
    
def NOTStopp(pin26):
    global NOTHALT, fehler
    anlage_ein = False
    fehler = 41
    ausrichtung_check.deinit()

btn_startstopp.irq(trigger=Pin.IRQ_FALLING, handler=ablauf)
btn_NOTStopp.irq(trigger=Pin.IRQ_FALLING, handler=NOTStopp)
