#ToDo: return false wenn endlage nicht erreicht wird
       
"""
die Pos. wir in grad übergeben

"""

from machine import Pin
from time import sleep,sleep_us
from Sonne import getSEA

#wieder löschen
#from _thread			import allocate_lock
#NOTHALT = allocate_lock()

ini_0geneigt   = Pin(18 , Pin.IN,Pin.PULL_UP)
ini_90geneigt  = Pin(17 , Pin.IN,Pin.PULL_UP)

hoch   = Pin(27 , Pin.IN,Pin.PULL_UP)
runter   = Pin(26 , Pin.IN,Pin.PULL_UP)

# Pins für den DRV8825 Schrittmotor-Treiber
DIR_PIN      = Pin(5, Pin.OUT,value =0)  # Richtungs-Pin 1 fährt hoch!
STEP_PIN     = Pin(6, Pin.OUT,value =0)  # Schritt-Pin
SLEEP_PIN    = Pin(7, Pin.OUT,value =0)  # Aktivierung des Treibers
PSU24V       = Pin(12 , Pin.OUT, value=0)
viertel_step = Pin(14 , Pin.OUT,value =0) # 0 = Full Step 1= 1/4 Step

micro_step_runter = 4 		#1/4
micro_step_hoch   = 1		#Full Step!
ratio             = 30		
time_step_runter  = 2500 	#in us
time_step_hoch 	  = 5000	#in us

max_steps_hoch  = round((90/1.8)*micro_step_hoch*ratio)
max_steps_runter= round((90/1.8)*micro_step_runter*ratio)


def neigen_kali(NOTHALT):
    print("Kalibrierung Neigen Achse")
    
    if ini_90geneigt.value()==0:
            #bereits in 90° Pos.
            return 0, 90
    else:
        DIR_PIN.value(1)
        PSU24V.value(1)    
        SLEEP_PIN.value(1)
        viertel_step.value(0)
        sleep(0.2)
    
    steps=0
    
    while ini_90geneigt.value()==1 and  NOTHALT.locked()==False and max_steps_hoch>steps:
        STEP_PIN.value(1)
        sleep_us(round(time_step_hoch/2))
        STEP_PIN.value(0)
        sleep_us(round(time_step_hoch/2))
        steps+=1
        
    SLEEP_PIN.value(0)    
    DIR_PIN.value(0)
    PSU24V.value(0)
    
    if NOTHALT.locked()==True: #Not-Aus ausgelöst
        return 41,999
    
    if max_steps_hoch-5<steps:
        print("zu viele Schritte, Pos. überprüfen!")
        return 10,999
    
    return 0,90


def neigen0(NOTHALT,pos):
    
    if ini_0geneigt.value() == 0:
        print("0° ist bereits angefahren!")
        return 0, 0
    
    print("Fahre 0° an!")

    #+3 grad damit Endlage safe angesprochen wird und Toleranzen ausgeglichen werden
    steps = round((pos/1.8)*micro_step_runter*ratio) #Schritte berechnen
    
    DIR_PIN.value(0)
    viertel_step.value(1)
    PSU24V.value(1)
    SLEEP_PIN.value(1)
    sleep(.2)
    
    for _ in range(steps):
        if NOTHALT.locked()== True:
            break
        STEP_PIN.value(1)
        sleep_us(round(time_step_runter/2)) 
        STEP_PIN.value(0)
        sleep_us(round(time_step_runter/2))
        if ini_0geneigt.value() == 0:
            print("Ini 0° geneigt betätigt")
            break
    
    sleep(.2)
    PSU24V.value(0)
    SLEEP_PIN.value(0)
    
    if NOTHALT.locked()== True:
        print("Not-Halt hat ausgelöst")
        return 41,999
    
    if ini_0geneigt.value() == 0:
        return 0,0
    else:
        return 12,999

#über 90 grad fahren!
def neigen90(NOTHALT, pos):
    
    if ini_90geneigt.value() == 0:
        print("90° ist bereits angefahren!")
        return 0, 90
    
    print("Fahre 90° an!")

    #+3 grad damit Endlage safe angesprochen wird und Toleranzen ausgeglichen werden
    dif = 90 - pos
    steps = round((dif+3/1.8)*micro_step_hoch*ratio) #Schritte berechnen
    print(steps)
    DIR_PIN.value(1)
    viertel_step.value(0)
    PSU24V.value(1)
    SLEEP_PIN.value(1)
    sleep(.2)
    
    for _ in range(steps):
        if NOTHALT.locked()== True:
            break
        STEP_PIN.value(1)
        sleep_us(round(time_step_hoch/2)) 
        STEP_PIN.value(0)
        sleep_us(round(time_step_hoch/2))
        if ini_90geneigt.value() == 0:
            print("Ini 90° geneigt betätigt")
            break
    print("fertig")
    sleep(.2)
    PSU24V.value(0)
    SLEEP_PIN.value(0)
    
    if NOTHALT.locked()== True:
        print("Not-Halt hat ausgelöst")
        return 41,999
    
    if ini_90geneigt.value() == 0:
        return 0,90
    else:
        return 11,999       
    
    
def neigen_sonne(NOTHALT, pos):

    print("Fahre Sonnenposition an!")
    print("Pos vor Fahrt: %i",pos)
    
    sonnen_pos = getSEA(51,7,2)
    #sonnen_pos = round(sonnen_pos)  Kontrollieren
    print("Sonnenhöhe: %i"%sonnen_pos)
    if sonnen_pos < 0:
        print("die Sonne ist noch nicht aufgegangen")
        return 0,pos
    
    if pos+1<sonnen_pos or pos-1<sonnen_pos:
        print("Steht noch +-1 in Sonnenposition")
        return 0,pos
    
    if pos<sonnen_pos: #hoch fahren
        dif = sonnen_pos-pos
        steps = round((dif/1.8)*micro_step_hoch*ratio)
        DIR_PIN.value(1)
        print("fahre hoch")
        viertel_step.value(0)
        time_step = time_step_hoch
        
    if pos>sonnen_pos: #runter fahren
        dif = pos-sonnen_pos
        print("Die differenz der pos. beträgt: %i"%dif)
        steps = round((dif/1.8)*micro_step_runter*ratio)    
        DIR_PIN.value(0)
        print("fahre runter")
        viertel_step.value(1)
        time_step = time_step_runter
        
    if NOTHALT.locked()== True:
        print("Not-Halt hat ausgelöst")
        return 41,999    
     
    PSU24V.value(1)
    SLEEP_PIN.value(1)
    sleep(.2)
    
    for _ in range(steps):
        if NOTHALT.locked()== True:
            break
        STEP_PIN.value(1)
        sleep_us(round(time_step/2)) 
        STEP_PIN.value(0)
        sleep_us(round(time_step/2))

        if ini_0geneigt.value() == 0 and DIR_PIN.value()==0 or ini_90geneigt.value() == 0 and DIR_PIN.value() == 1:
            print("Eine Endlage Neigen wurde betätigt")
            break
    
    sleep(.2)
    PSU24V.value(0)
    SLEEP_PIN.value(0)
    
    if NOTHALT.locked()== True:
        print("Not-Halt hat ausgelöst")
        return 41,999
    
    if ini_90geneigt.value() == 0:
        return 10,90
    if ini_0geneigt.value() == 0:
        return 10,0
    
    return 0,sonnen_pos #wenn alles gut ist


def neigen_hand(NOTHALT, pos):
    
    while not(hoch.value()==0 and runter.value()==0):
        first_run_hoch   = True
        schleife_hoch    = False
        first_run_runter = True
        schleife_runter  = False        
        
        #Hoch Handbetrieb
        while hoch.value()==0 and ini_90geneigt.value()==1 and runter.value()==1:
            
            if NOTHALT.locked()== True:
                break
            
            if first_run_hoch == True:
                first_run_hoch = False
                schleife_hoch = True
                viertel_step.value(0)
                DIR_PIN.value(1) 
                PSU24V.value(1)
                SLEEP_PIN.value(1)
                sleep(.2)
                
            STEP_PIN.value(1)
            sleep_us(round(time_step_hoch/2)) 
            STEP_PIN.value(0)
            sleep_us(round(time_step_hoch/2))
            if ini_90geneigt.value() == 0:
                print("Ini 90° geneigt betätigt")
                break
            
        if schleife_hoch == True:
            schleife_hoch = False
            sleep(.1)
            PSU24V.value(0)
            SLEEP_PIN.value(0)
            sleep(.2)
        
        #Runter Handbetrieb
        while runter.value()==0 and ini_0geneigt.value()==1 and hoch.value()==1:
            
            if NOTHALT.locked()== True:
                break
            
            if first_run_runter == True:
                first_run_runter = False
                schleife_runter = True
                viertel_step.value(1)
                DIR_PIN.value(0) 
                PSU24V.value(1)
                print("spannung an")
                SLEEP_PIN.value(1)
                sleep(.5)
                
            STEP_PIN.value(1)
            sleep_us(round(time_step_runter/2)) 
            STEP_PIN.value(0)
            sleep_us(round(time_step_runter/2))
            if ini_0geneigt.value() == 0:
                print("Ini 0° geneigt betätigt")
                break
            
        if schleife_runter == True:
            schleife_runter = False
            sleep(.1)
            PSU24V.value(0)
            print("spannung weg genommen")
            SLEEP_PIN.value(0)
            sleep(.2)
        
#Endlage wieder hinzufügen!! Hand!        
#neigen_hand(NOTHALT,0)         
#neigen90(NOTHALT,0)
#sleep(1)
#neigen_sonne(NOTHALT,90)
#sleep(5)
#neigen0(NOTHALT,88)
#neigen_sonne()
#neigen_kali(NOTHALT)            
