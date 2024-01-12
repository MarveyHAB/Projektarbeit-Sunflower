import veml7700
import ds1307
from hmc5883l import HMC5883L
from _thread import allocate_lock
from sonne_jan import getAZ, getSEA
from drehen import drehen_grundpos, drehen_sonne, drehen_kali
from neigen import neigen0, neigen90, neigen_sonne, neigen_kali
from faechern import auffaechern, einfaechern, faechern_kali
from machine import Pin, RTC, SoftI2C, Timer
from time import sleep, sleep_ms
from Manuelle Steuerung import manuel

#Allocate Lock
NOTHALT = allocate_lock()

#Timer
ausrichtung_check = Timer()

#BTN
btn_startstopp    	= Pin(27 , Pin.IN,Pin.PULL_UP)
btn_ISR_NOTHALT      	= Pin(26 , Pin.IN,Pin.PULL_UP)
#btn_einfahren     	= Pin(22 , Pin.IN,Pin.PULL_UP)
ini_ausgefaechert 	= Pin(21 , Pin.IN,Pin.PULL_UP)
ausrichten_freigabe = False
anlage_ein        	= False
status_automatik	= False
fehler				= 0
anlage_ist_aus		= True
state_1 			= True  #Einfächern 
state_2 			= False #
state_3 			= False
state_4 			= False
state_5 			= False
state_6 			= False
state_7 			= False
state_8 			= False
state_9 			= False
state_10			= False

#Speicher Positionen
pos_neigen = 0
pos_drehen = 0



#manuelle verfahrung.
def second_thread():
    manuel()

start_new_thread(second_thread, ())
#-------------------------------------

def ISR_ausrichtung(abc):
    global state_9, ausrichten_freigabe
    stat_9 				= True
    ausrichten_freigabe = True

def ISR_ein_aus(pin22):
    global anlage_ein, fehler, NOTHALT
    
    if NOTHALT.locked() == True:
        i += 1
        if i == 2:
            NOTHALT.release()
            print("Nothalt wurde quittiert! Anlage kalibriert neu!")
            i = 0
            state_1 			= True   
            state_2 			= False 
            state_3 			= False
            state_4 			= False
            state_5 			= False
            state_6 			= False
            state_7 			= False
            state_8 			= False
            state_9 			= False
            state_10			= False
    else:
        anlage_ein = not anlage_ein
        
    
    if fehler != 0: 
        #Was soll passieren wenn fehler True????????
        ausrichtung_check.deinit()
        #11 = Fehler aufneigen,  12 = Fehler zuneigen        
        #21 = Fehler auffächern, 22 = Fehler zufächern
        #31 = Fehler drehen
        #41 = NOTHALT
    
def ISR_NOTHALT(pin26):
    global NOTHALT, fehler, anlage_ein
    anlage_ein = False
    ausrichtung_check.deinit()
    fehler = 41
    
    NOTHALT.acquire()
    print("NOTHALT Ausgelöst!")

def ISR_ausrichtung(abc):
    stat_9 = True
    

btn_startstopp.irq(trigger=Pin.IRQ_FALLING, handler=ISR_ein_aus)
btn_ISR_NOTHALT.irq(trigger=Pin.IRQ_FALLING, handler=ISR_NOTHALT)



while True:
    #Wird nur ausgefürt nach Hardreset oder NOTHALT!
    if state_1 == True and NOTHALT == False and anlage_ein = True:
            rueckgabe_neigen = neigen_kali(NOTHALT)
            if rueckgabe[0]== 0:
                state_1 = False
                state_2 = True
                anlage_ist_aus = False
                pos_neigen = rueckgabe_neigen[1]
            elif if rueckgabe[0]== 13:
                print("Zu viele schritte beim Neigen gefahren. Position Überprüfen!")
                fehler = 13
                analge_ein = False
                

    if state_2 == True and NOTHALT == False and anlage_ein = True:
            if faechern_kali(NOTHALT) == True:
                state_2 = False
                state_3 = True
    
    if state_3 == True and NOTHALT == False and anlage_ein = True:
            rueckgabe_drehen = drehen_kali(NOTHALT)
            if rueckgabe_drehen[0] == True:
                state_3 = False
                state_4 = True
                pos_drehen = rueckgabe_drehen[1]
                
#Wenn alle in Grundposition kalibriert sind.
    if state_4 == True and NOTHALT == False and anlage_ein = True:
        rueckgabe_neigen90 = neigen90(NOTHALT, pos_neigen)
        if  rueckgabe_neigen90[0] == 0:
                print("Endlage neigen errreicht.")
                state_4 = False
                state_5 = True
                anlage_ist_aus = False
                pos_neigen = rueckgabe_neigen90[1]
        elif  rueckgabe_neigen90[0] == 11:
                print("Timeout! Endlage beim zuneigen konnte nicht errreicht werden!")
                anlage_ein = False
                fehler = 11
        else  rueckgabe_neigen90[0] == 12:
                print("Timeout! Endlage beim aufneigen konnte nicht errreicht werden!")
                anlage_ein = False
                fehler = 12
    
    if state_5 == True and NOTHALT == False and anlage_ein = True:
        rueckgabe_auffächern = auffaechern(NOTHALT)
        if rueckgabe_auffächern != 0:
                print("Timeout! Endlage Auffächern konnte nicht errreicht werden!")
                anlage_ein = False
                fehler = 21
        else:
            state_5 = False
            state_6 = True

    if state_6 == True and NOTHALT == False and anlage_ein = True:
        rueckgabe_drehen_sonne = drehen_sonne(NOTHALT, pos_drehen)
        if  rueckgabe_drehen_sonne[0] != 0:
            print("Timeout! Position Drehen konnte nicht errreicht werden!")
            anlage_ein = False
            fehler = 31
        else:
            state_6 = False
            state_7 = True
            pos_drehen = rueckgabe_drehen_sonne[1]

    if state_7 == True and NOTHALT == False and anlage_ein = True:
        rueckgabe_neigen_sonne = neigen_sonne(NOTHALT, pos_neigen)
        if rueckgabe_neigen_sonne[0] != 0:
                print("Timeout! Position neigen konnte nicht errreicht werden!")
                anlage_ein = False
                fehler = 10
        else:
            state_7 = False
            state_8 = True
            pos_neigen = rueckgabe_neigen_sonne[1]

    if state_8 == True and NOTHALT == False and anlage_ein = True:
        if status_automatik== False:
            ausrichtung_check.init(period=120000 , mode=Timer.PERIODIC, callback=ISR_ausrichtung)
            print("Automatik Betrieb gestartet!")
            state_8 			= False
            state_9 			= True
            status_automatik 	= True
        else:
            state_8 = False
            state_9 = True

    if state_9 == True and NOTHALT == False and anlage_ein = True:
        if ausrichten_freigabe == True:
            print("Automatische Ausrichtung.")
            
            rueckgabe_neigen_sonne = drehen_sonne(NOTHALT, pos_neigen)
            if rueckgabe_neigen_sonne[0] == 10:
                print("Fehler neigen Sonne!")
                fehler = 10
                analage_ein = False
            else:
                pos_neigen = rueckgabe_neigen_sonne[1]
            
            if fehler == 0:
                rueckgabe_drehen_sonne = neigen_sonne(NOTHALT, pos_drehen)
            if rueckgabe_drehen_sonne[0] == 20:
                print("Fehler Sonne drehen!")
                fehler = 20
                analge_ein = False
            else:
                pos_drehen = rueckgabe_drehen_sonne[1]
                state_9 			= False
                stat_10 			= True
                ausrichten_freigabe	= False
        else:
            state_9 			= False
            stat_10 			= True

    #Ausschalten    
    if state_10 == True and NOTHALT == False and anlage_ein = False:
        if anlage_ist_aus == False:
            print("SunFlower wird ausgeschalten.")
            ausrichtung_check.deinit()
            
            rueckgabe_neigen_90 = neigen90(NOTHALT, pos_neigen)
            if rueckgabe_neigen_90[0] != 0:
                print("fehler neigen Parken")
                fehler = 11
            else fehler == 0:
                pos_drehen = rueckgabe_neigen_90[1]
                rueckgabe_drehen = drehen_grundpos(NOTHALT, pos_drehen)
                if rueckgabe_drehen[0] =! 0:
                    print("Fehler drehen Parken!")
                    fehler = 31
                else fehler == 0:
                    pos_drehen = rueckgabe_drehen[1]
                    rueckgabe_faechern = einfaechern(NOTHALT)
                    if rueckgabe_faechern[0] != 0:
                        print("fehler einfächern Parken")
                        fehler = 22
                    else fehler == 0:
                        rueckgabe_neigen_0 = neigen0(NOTHALT, pos_neigen)
                        if rueckgabe_neigen_0[0] !=0:
                            print("Fehler neigen Parken")
                            fehler = 12
                        else fehler == 0:
                            print("Parkposition erreicht")
                            state_10 			= False
                            state_8				= True
                            status_automatik 	= False
                            anlage_ist_aus		= True
                            
    else:
        state_10 			= False
        state_8				= True
