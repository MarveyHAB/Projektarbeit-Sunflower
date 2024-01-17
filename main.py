import ds1307
from sh1106 	import SH1106_I2C
from hmc5883l	import HMC5883L
from _thread	import allocate_lock
from Sonne		import getAZ, getSEA
from drehen		import drehen_grundpos, drehen_sonne, drehen_kali
from neigen		import neigen0, neigen90, neigen_sonne, neigen_kali
from faechern	import auffaechern, einfaechern, faechern_kali
from machine	import Pin, RTC, I2C, Timer
from time		import sleep, sleep_ms

#Display
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
display = SH1106_I2C(128, 64, i2c, Pin(28), 0x3c)

display.fill(0)
display.text('Sunflower ', 30, 20, 1)
display.text('bereit!'   , 40, 30, 1)
display.show()

#Allocate Lock
NOTHALT = allocate_lock()

#Timer
ausrichtung_check = Timer()

#BTN
btn_startstopp		= Pin(27 , Pin.IN,Pin.PULL_UP)
btn_ISR_NOTHALT		= Pin(26 , Pin.IN,Pin.PULL_UP)

fehler				= 0
ausrichten_freigabe = False
anlage_ein        	= False
status_automatik	= False
anlage_ist_aus		= True
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

#Speicher Positionen
pos_neigen 			= 0
pos_drehen 			= 0



def ISR_ausrichtung(abc):
    global state_9, ausrichten_freigabe
    stat_9 				= True
    ausrichten_freigabe = True

def ISR_ein_aus(pin22):
    global anlage_ein, fehler, NOTHALT
    
    #Nothalt Quittieren
    if NOTHALT.locked() == True:
        i += 1
        if i == 2:
            NOTHALT.release()
            print("Nothalt wurde quittiert! Anlage kalibriert neu!")
            
            display.fill(0)
            display.text('Nothalt wurde ' , 0, 0, 1)
            display.text('quittiert.'     , 0, 10, 1)
            display.text('Sunflower'      , 0, 20, 1)
            display.text('kalibriert neu!', 0, 30, 1)
            display.show()
            
            i = 0
            sleep(2)
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
        
    #Fehler Quittieren
    elif fehler != 0:
        q += 1
        if q == 2:
            print("Fehler wurde quittiert! Anlage kalibriert neu!")
            display.fill(0)
            display.text('Fehler wurde ' , 0, 0, 1)
            display.text('quittiert.'     , 0, 10, 1)
            display.text('Sunflower'      , 0, 20, 1)
            display.text('kalibriert neu!', 0, 30, 1)
            display.show()
            
            fehler ==0
            q = 0
            sleep(2)
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
    
def ISR_NOTHALT(pin26):
    global NOTHALT, fehler, anlage_ein
    anlage_ein = False
    ausrichtung_check.deinit()
    fehler = 41
    
    NOTHALT.acquire()
    print("NOTHALT Ausgelöst!")
    display.fill(0)
    display.text('NOTHALT', 0, 0, 1)
    display.text('Ausgeloest!', 0, 10, 1)
    display.show()


btn_startstopp.irq(trigger=Pin.IRQ_FALLING, handler=ISR_ein_aus)
btn_ISR_NOTHALT.irq(trigger=Pin.IRQ_FALLING, handler=ISR_NOTHALT)



while True:
    #Wird nur ausgefürt nach Hardreset oder NOTHALT oder Fehler!
    if state_1 == True and NOTHALT == False and anlage_ein = True and fehler == 0:
        display.fill(0)
        display.text('Kalibrierung', 0, 0, 1)
        display.text('neigen laeuft', 0, 10, 1)
        display.show()
        
        rueckgabe_neigen = neigen_kali(NOTHALT)
        if rueckgabe[0]!= 0:
            fehler 			= rueckgabe[0]
            analge_ein 		= False
        else:
            state_1 		= False
            state_2 		= True
            anlage_ist_aus 	= False
            pos_neigen 		= rueckgabe_neigen[1]
                
                
    if state_2 == True and NOTHALT == False and anlage_ein = True and fehler == 0:
        display.fill(0)
        display.text('Kalibrierung'    , 0, 0, 1)
        display.text('faechern laeuft', 0, 10, 1)
        display.show()
        if faechern_kali(NOTHALT) != 0:
            fehler 		= faechern_kali
            analge_ein 		= False
        else:
            state_2 	= False
            state_3 	= True
    
    if state_3 == True and NOTHALT == False and anlage_ein = True and fehler == 0:
        display.fill(0)
        display.text('Kalibrierung'    , 0, 0, 1)
        display.text('drehen laeuft', 0, 10, 1)
        display.show()
        rueckgabe_drehen = drehen_kali(NOTHALT)
        if rueckgabe_drehen[0] != 0:
            fehler 			= rueckgabe_drehen[0]
            analge_ein 		= False
        else:
            state_3 	= False
            state_4 	= True
            pos_drehen 	= rueckgabe_drehen[1]
                
#Wenn alle in Grundposition kalibriert sind.
    if state_4 == True and NOTHALT == False and anlage_ein = True and fehler == 0:
        display.fill(0)
        display.text('State 4', 0, 0, 1)
        display.show()
        rueckgabe_neigen90 = neigen90(NOTHALT, pos_neigen)
        if  rueckgabe_neigen90[0] != 0:
            fehler = rueckgabe_neigen90[0]
            anlage_ein 	= False
        else:
            state_4 	= False
            state_5 	= True
            pos_neigen 	= rueckgabe_neigen90[1]
            
    
    if state_5 == True and NOTHALT == False and anlage_ein = True and fehler == 0:
        display.fill(0)
        display.text('State 5', 0, 0, 1)
        display.show()
        rueckgabe_auffächern = auffaechern(NOTHALT)
        if rueckgabe_auffächern != 0:
            fehler 		= rueckgabe_auffächern
            anlage_ein 	= False
                
        else:
            state_5 	= False
            state_6 	= True

    if state_6 == True and NOTHALT == False and anlage_ein = True and fehler == 0:
        display.fill(0)
        display.text('State 6', 0, 0, 1)
        display.show()
        rueckgabe_drehen_sonne = drehen_sonne(NOTHALT, pos_drehen)
        if  rueckgabe_drehen_sonne[0] != 0:
            fehler 		= rueckgabe_drehen_sonne[0]
            anlage_ein 	= False
        else:
            state_6 	= False
            state_7 	= True
            pos_drehen 	= rueckgabe_drehen_sonne[1]

    if state_7 == True and NOTHALT == False and anlage_ein = True and fehler == 0:
        display.fill(0)
        display.text('State 7', 0, 0, 1)
        display.show()
        rueckgabe_neigen_sonne = neigen_sonne(NOTHALT, pos_neigen)
        if rueckgabe_neigen_sonne[0] != 0:
            fehler		= rueckgabe_neigen_sonne[0]
            anlage_ein 	= False

        else:
            state_7 	= False
            state_8 	= True
            pos_neigen 	= rueckgabe_neigen_sonne[1]

    if state_8 == True and NOTHALT == False and anlage_ein = True and fehler == 0:
        display.fill(0)
        display.text('State 8', 0, 0, 1)
        display.show()
        if status_automatik== False:
            ausrichtung_check.init(period=120000 , mode=Timer.PERIODIC, callback=ISR_ausrichtung)
            print("Automatik Betrieb aktiviert!")
            display.fill(0)
            display.text('Sunflower', 0,  0, 1)
            display.text('Automatikbetrieb'   , 0, 10, 1)
            display.text('aktiviert.'  , 0, 20, 1)
            display.show()
            state_8 			= False
            state_9 			= True
            status_automatik 	= True
        else:
            state_8 			= False
            state_9 			= True

    if state_9 == True and NOTHALT == False and anlage_ein = True and fehler == 0:
        display.fill(0)
        display.text('State 9', 0, 0, 1)
        display.show()
        if ausrichten_freigabe == True:
            print("Automatische Ausrichtung.")
            display.fill(0)
            display.text('Sunflower wird.', 0,  0, 1)
            display.text('automatisch.'   , 0, 10, 1)
            display.text('ausgerichtet.'  , 0, 20, 1)
            display.show()
            
            rueckgabe_neigen_sonne = drehen_sonne(NOTHALT, pos_neigen)
            if rueckgabe_neigen_sonne[0] != 0:
                fehler 				= rueckgabe_neigen_sonne[0]
                analage_ein 		= False
                ausrichten_freigabe	= False
            else:
                pos_neigen = rueckgabe_neigen_sonne[1]
            
            if fehler == 0:
                rueckgabe_drehen_sonne = neigen_sonne(NOTHALT, pos_drehen)
                
            if rueckgabe_drehen_sonne[0] != 0:
                fehler 				= rueckgabe_drehen_sonne[0]
                analge_ein 			= False
                ausrichten_freigabe	= False
            else:
                pos_drehen = rueckgabe_drehen_sonne[1]
                state_9 			= False
                stat_10 			= True
                ausrichten_freigabe	= False
        else:
            state_9 			= False
            stat_10 			= True

    #Ausschalten    
    if state_10 == True and NOTHALT == False and anlage_ein = False and fehler == 0:
        if anlage_ist_aus == False:
            display.fill(0)
            display.text('Sunflower wird.', 0,  0, 1)
            display.text('ausgeschalten.' , 0, 10, 1)
            display.show()
            print("SunFlower wird ausgeschalten.")
            ausrichtung_check.deinit()
            
            rueckgabe_neigen_90 = neigen90(NOTHALT, pos_neigen)
            if rueckgabe_neigen_90[0] != 0:
                fehler = rueckgabe_neigen_90[0]
            else fehler == 0:
                pos_neigen 			= rueckgabe_neigen_90[1]
                rueckgabe_drehen 	= drehen_grundpos(NOTHALT, pos_drehen)
                if rueckgabe_drehen[0] =! 0:
                    fehler = rueckgabe_drehen[0]
                else fehler == 0:
                    pos_drehen 			= rueckgabe_drehen[1]
                    rueckgabe_faechern 	= einfaechern(NOTHALT)
                    if rueckgabe_faechern[0] != 0:
                        fehler = rueckgabe_faechern[0]
                    else fehler == 0:
                        rueckgabe_neigen_0 = neigen0(NOTHALT, pos_neigen)
                        if rueckgabe_neigen_0[0] !=0:
                            fehler = rueckgabe_neigen_0[0]
                        else fehler == 0:
                            print("Parkposition erreicht")
                            display.fill(0)
                            display.text('Parkposition', 0,  0, 1)
                            display.text('erreicht'    , 0, 10, 1)
                            display.show()
                            pos_neigen 			= rueckgabe_neigen_0[1]
                            state_10 			= False
                            state_8				= True
                            status_automatik 	= False
                            anlage_ist_aus		= True
                            
    else:
        state_10 			= False
        state_8				= True
    
    if fehler != 0:
        if fehler == 10:
            print("Fehler Kalibrierung neigen")
            display.fill(0)
            display.text('Fehler'      , 0,  0, 1)
            display.text('Kalibrierung', 0, 10, 1)
            display.text('neigen'      , 0, 20, 1)
            display.show()
        elif fehler == 11:
            print("Fehler aufneigen")
            display.fill(0)
            display.text('Fehler aufneigen', 0, 0, 1)
            display.show()
        elif fehler == 12:
            print("Fehler zuneigen")
            display.fill(0)
            display.text('Fehler zuneigen', 0, 0, 1)
            display.show()
        elif fehler == 20:
            print("Fehler Kalibrierung fächern")
            display.fill(0)
            display.text('Fehler'      , 0,  0, 1)
            display.text('Kalibrierung', 0, 10, 1)
            display.text('faechern'    , 0, 20, 1)
            display.show()
        elif fehler == 21:
            print("Fehler auffächern")
            display.fill(0)
            display.text('Fehler'     , 0,  0, 1)
            display.text('auffaechern', 0, 10, 1)
            display.show()
        elif fehler == 22:
            print("Fehler zufächern")
            display.fill(0)
            display.text('Fehler', 0,  0, 1)
            display.text('zufaechern', 0, 10, 1)
            display.show()
        elif fehler == 30:
            print("Fehler Kalibrierung Drehen")
            display.fill(0)
            display.text('Fehler'      , 0,  0, 1)
            display.text('Kalibrierung', 0, 10, 1)
            display.text('drehen'      , 0, 20, 1)
            display.show()
        elif fehler == 31:
            print("Fehler drehen")
            display.fill(0)
            display.text('Fehler drehen', 0, 0, 1)
            display.show()
        else fehler == 41:
            print("Nothalt ausgelöst!")
            display.fill(0)
            display.text('Nothalt'   , 0,  0, 1)
            display.text('betaetigt!', 0, 10, 1)
            display.show()
