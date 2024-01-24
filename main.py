#TODO
#Kompass
from sh1106 	import SH1106_I2C
from _thread	import allocate_lock
from drehen_ohne_kompass		import drehen_grundpos, drehen_sonne, drehen_kali
from neigen		import neigen0, neigen90, neigen_sonne, neigen_kali
from faechern	import auffaechern, einfaechern, faechern_kali
from machine	import Pin, RTC, I2C, Timer
from time		import sleep, sleep_ms, ticks_ms
from RTC 		import sync_RTC_Pico_time
from Sonne 		import getSEA # <0 Sonne nicht aufgegangen #sonnen_pos = getSEA(51,7,2)
from errorcode	import fehlermeldung
#Zeit mit RTC sync
sync_RTC_Pico_time()

#Display
i2c 	= I2C(0, scl=Pin(1), sda=Pin(0))
display	= SH1106_I2C(128, 64, i2c, Pin(28), 0x3c)

display.sleep(False)
display.fill(0)
display.text('Sunflower ', 30, 20, 1)
display.text('bereit!'   , 40, 30, 1)
display.show()

#Allocate Lock
NOTHALT = allocate_lock()

#BTN
btn_startstopp	= Pin(27 , Pin.IN,Pin.PULL_UP)
btn_NOTHALT		= Pin(26 , Pin.IN,Pin.PULL_UP)

#State
fehler				= 0
ausrichten_freigabe	= False
anlage_ein        	= False
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

#BTN entprellen
push_ein_aus 		= 0
push_ein_aus_old 	= 0

push_nothalt 		= 0
push_nothalt_old 	= 0

i = 0
q = 0

#Speicher Positionen
pos_neigen 			= 0
pos_drehen 			= 0

#Sonnen Position
sonnen_pos = getSEA(51,7,2)


def ISR_ein_aus(hallo):
    global anlage_ein, fehler, NOTHALT, push_ein_aus, push_ein_aus_old, i, q
    push_ein_aus_old = push_ein_aus
    push_ein_aus = ticks_ms()
    
    if push_ein_aus - push_ein_aus_old > 250:
        
        #Nothalt Quittieren
        if NOTHALT.locked() == True:
            i += 1
            print(i)
            if i == 2:
                NOTHALT.release()
                fehler = 0
                print("Nothalt wurde quittiert! Anlage kalibriert neu!")
                
                display.fill(0)
                display.text('Nothalt wurde ' , 0, 0, 1)
                display.text('quittiert.'     , 0, 10, 1)
                display.text('Sunflower'      , 0, 20, 1)
                display.text('kalibriert neu!', 0, 30, 1)
                display.show()
                
                i = 0
                sleep(2)
                state_1 = True   
            
        #Fehler Quittieren
        elif fehler != 0:
            q += 1
            print(q)
            if q == 2:
                print("Fehler wurde quittiert! Anlage kalibriert neu!")
                display.fill(0)
                display.text('Fehler wurde ' , 0, 0, 1)
                display.text('quittiert.'     , 0, 10, 1)
                display.text('Sunflower'      , 0, 20, 1)
                display.text('kalibriert neu!', 0, 30, 1)
                display.show()
                
                fehler = 0
                q = 0
                sleep(2)
                state_1 = True   

        else:
            anlage_ein = not anlage_ein
            print(anlage_ein)
            #if anlage_ein == False:
            #    state_10 = True

    
def ISR_NOTHALT(abcde):
    global NOTHALT, fehler, anlage_ein, push_nothalt, push_nothalt_old
    push_nothalt_old = push_nothalt
    push_nothalt = ticks_ms()
    
    if push_nothalt - push_nothalt_old > 250:
        anlage_ein	= False
        fehler 		= 41
        state_1 	= False   
        state_2 	= False 
        state_3 	= False
        state_4 	= False
        state_5 	= False
        state_6 	= False
        state_7 	= False
        state_8 	= False
        state_9 	= False
        state_10	= False
        
        NOTHALT.acquire()
        
        display.fill(0)
        display.text('NOTHALT', 0, 0, 1)
        display.text('Ausgeloest!', 0, 10, 1)
        display.show()
        print("NOTHALT Ausgelöst!")


btn_startstopp.irq(trigger=Pin.IRQ_RISING, handler=ISR_ein_aus)
btn_NOTHALT.irq(trigger=Pin.IRQ_RISING, handler=ISR_NOTHALT)



while True:
    sleep(.2)
    #Wird nur ausgefürt nach Hardreset oder NOTHALT oder Fehler!
    if state_1 == True and NOTHALT.locked() == False and anlage_ein == True and fehler == 0:
        display.fill(0)
        display.text('Kalibrierung', 0, 0, 1)
        display.text('neigen laeuft', 0, 10, 1)
        display.show()
        
        rueckgabe_neigen = neigen_kali(NOTHALT)
        if rueckgabe_neigen[0]!= 0:
            fehler 			= rueckgabe_neigen[0]
            analge_ein 		= False
        else:
            state_1 		= False
            state_2 		= True
            anlage_ist_aus 	= False
            pos_neigen 		= rueckgabe_neigen[1]
                
    if state_2 == True and NOTHALT.locked() == False and anlage_ein == True and fehler == 0:
        display.fill(0)
        display.text('Kalibrierung'    , 0, 0, 1)
        display.text('faechern laeuft', 0, 10, 1)
        display.show()
        if faechern_kali(NOTHALT) != 0:
            fehler 		= faechern_kali
            analge_ein 	= False
            state_2 	= False
        else:
            state_2 	= False
            state_3 	= True
    
    if state_3 == True and NOTHALT.locked() == False and anlage_ein == True and fehler == 0:
        display.fill(0)
        display.text('Kalibrierung'    , 0, 0, 1)
        display.text('drehen laeuft', 0, 10, 1)
        display.show()
        rueckgabe_drehen = drehen_kali(NOTHALT)
        if rueckgabe_drehen[0] != 0:
            fehler 		= rueckgabe_drehen[0]
            analge_ein 	= False
            state_3 	= False
            #print("drehen mit fehler")
        else:
            if sonnen_pos >0:
                state_3 	= False
                state_4 	= True
                pos_drehen 	= rueckgabe_drehen[1]
            else:
                analge_ein 	= False
                state_3 	= False
                state_10 	= True
                
#Wenn alle in Grundposition kalibriert sind.
    if state_4 == True and NOTHALT.locked() == False and anlage_ein == True and fehler == 0 and sonnen_pos >0:
        display.fill(0)
        display.text('Neigen zum ', 0,  0, 1)
        display.text('Auffaechern', 0, 10, 1)
        display.show()
        rueckgabe_neigen90 = neigen90(NOTHALT, pos_neigen)
        if  rueckgabe_neigen90[0] != 0:
            fehler = rueckgabe_neigen90[0]
            anlage_ein 	= False
            state_4 	= False
        else:
            state_4 	= False
            state_5 	= True
            pos_neigen 	= rueckgabe_neigen90[1]
    elif state_4 == True and sonnen_pos >0:
        state_4  = False
        state_10 = True
            
    
    if state_5 == True and NOTHALT.locked() == False and anlage_ein == True and fehler == 0 and sonnen_pos >0:
        display.fill(0)
        display.text('Auffaechern', 0, 0, 1)
        display.show()
        rueckgabe_auffächern = auffaechern(NOTHALT)
        if rueckgabe_auffächern != 0:
            fehler 		= rueckgabe_auffächern
            anlage_ein 	= False
            state_5 	= False
            print("Fächern mit fehler")
            print(fehler)
                
        else:
            state_5 	= False
            state_6 	= True
            print("Fächern ohne fehler")

    if state_6 == True and NOTHALT.locked() == False and anlage_ein == True and fehler == 0 and sonnen_pos >0:
        display.fill(0)
        display.text('Drehen Sonne', 0, 0, 1)
        display.show()
        rueckgabe_drehen_sonne = drehen_sonne(NOTHALT, pos_drehen)
        if  rueckgabe_drehen_sonne[0] != 0:
            fehler 		= rueckgabe_drehen_sonne[0]
            anlage_ein 	= False
            state_6 	= False
        else:
            state_6 	= False
            state_7 	= True
            pos_drehen 	= rueckgabe_drehen_sonne[1]

    if state_7 == True and NOTHALT.locked() == False and anlage_ein == True and fehler == 0 and sonnen_pos >0:
        display.fill(0)
        display.text('Neigen Sonne', 0, 0, 1)
        display.show()
        rueckgabe_neigen_sonne = neigen_sonne(NOTHALT, pos_neigen)
        if rueckgabe_neigen_sonne[0] != 0:
            fehler		= rueckgabe_neigen_sonne[0]
            anlage_ein 	= False
            state_7 	= False

        else:
            state_7 	= False
            state_8 	= True
            pos_neigen 	= rueckgabe_neigen_sonne[1]
            zeit_alt 	= ticks_ms()

    if state_8 == True and NOTHALT.locked() == False and anlage_ein == True and fehler == 0 and sonnen_pos >0:
        print("state 8")
        zeit_neu = ticks_ms()
        wartezeit = (10000 - (zeit_neu - zeit_alt)) / 1000
        
        display.fill(0)
        display.text('Zeit bis', 0,  0, 1)
        display.text('automitischer'   , 0, 10, 1)
        display.text('ausrichtung: %is.' %wartezeit  , 0, 20, 1)
        display.show()
        
        if zeit_neu - zeit_alt >= 10000:
            zeit_alt			= zeit_neu
            state_8 			= False
            state_9 			= True
            ausrichten_freigabe = True

        else:
            state_8 			= False
            state_9 			= True

    if state_9 == True and NOTHALT.locked() == False and anlage_ein == True and fehler == 0 and sonnen_pos >0:
        print("state 9")
        if ausrichten_freigabe == True:
            ausrichten_freigabe = False
            print("Automatische Ausrichtung.")
            display.fill(0)
            display.text('Sunflower wird.', 0,  0, 1)
            display.text('automatisch.'   , 0, 10, 1)
            display.text('ausgerichtet.'  , 0, 20, 1)
            display.show()
            
            rueckgabe_neigen_sonne = neigen_sonne(NOTHALT, pos_neigen)
            if rueckgabe_neigen_sonne[0] != 0:
                fehler 		= rueckgabe_neigen_sonne[0]
                analage_ein	= False
                state_9 	= False
            else:
                pos_neigen = rueckgabe_neigen_sonne[1]
            
            if fehler == 0:
                rueckgabe_drehen_sonne = drehen_sonne(NOTHALT, pos_drehen)
                
            if rueckgabe_drehen_sonne[0] != 0:
                fehler 		= rueckgabe_drehen_sonne[0]
                analge_ein 	= False
                state_9 	= False
            else:
                pos_drehen = rueckgabe_drehen_sonne[1]
                state_9 			= False
                state_10 			= True
        else:
            state_9 			= False
            state_10 			= True

    else:
        state_9 			= False
        state_10 			= True

    #Ausschalten    
    if state_10 == True and NOTHALT.locked() == False and fehler == 0:
        if (anlage_ein == False or sonnen_pos <0) and anlage_ist_aus == False:
            if anlage_ein == False:
                display.fill(0)
                display.text('Sunflower wird', 0,  0, 1)
                display.text('ausgeschalten.' , 0, 10, 1)
                display.show()
            elif sonnen_pos <0:
                display.fill(0)
                display.text('Sunflower wird', 0,  0, 1)
                display.text('Sonnenstand-'  , 0, 10, 1)
                display.text('bedingt .'     , 0, 20, 1)
                display.text('ausgeschaltet.' , 0, 30, 1)
                display.show()
                            
            rueckgabe_neigen_90 = neigen90(NOTHALT, pos_neigen)
            if rueckgabe_neigen_90[0] != 0:
                fehler = rueckgabe_neigen_90[0]
            elif fehler == 0:
                pos_neigen 			= rueckgabe_neigen_90[1]
                rueckgabe_drehen 	= drehen_grundpos(NOTHALT, pos_drehen)
                if rueckgabe_drehen[0] != 0:
                    fehler = rueckgabe_drehen[0]
                elif fehler == 0:
                    pos_drehen 			= rueckgabe_drehen[1]
                    rueckgabe_faechern 	= einfaechern(NOTHALT)
                    if rueckgabe_faechern != 0:
                        fehler = rueckgabe_faechern
                    elif fehler == 0:
                        rueckgabe_neigen_0 = neigen0(NOTHALT, pos_neigen)
                        if rueckgabe_neigen_0[0] !=0:
                            fehler = rueckgabe_neigen_0[0]
                        elif fehler == 0:
                            print("Parkposition erreicht")
                            display.fill(0)
                            display.text('Parkposition', 0,  0, 1)
                            display.text('erreicht'    , 0, 10, 1)
                            display.show()
                            pos_neigen 		= rueckgabe_neigen_0[1]
                            state_10 		= False
                            state_4			= True
                            anlage_ist_aus 	= True
                            
        elif anlage_ein == True:
            state_8  = True
            state_10 = False
            print("state 10 else")
    
    if fehler != 0:
        fehlermeldung(fehler)

