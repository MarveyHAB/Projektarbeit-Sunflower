#ToDo: return false wenn endlage nicht erreicht wird
       
"""
die Pos. wir in grad übergeben

"""

from machine import Pin, SPI
from time import sleep,sleep_us
from Sonne import getSEA
from TMC5160 import TMC5160
#Löschen
#from _thread	import allocate_lock
#NOTHALT = allocate_lock()
#ende löschen

#SPI Stepper
spi = SPI(0, baudrate=4000000, bits=8, firstbit=SPI.MSB, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
stepper = TMC5160(spi, 28, 0)

ini_0geneigt   = Pin(14 , Pin.IN,Pin.PULL_UP)
ini_90geneigt  = Pin(17 , Pin.IN,Pin.PULL_UP)

hoch     = Pin(27 , Pin.IN,Pin.PULL_UP)
runter   = Pin(26 , Pin.IN,Pin.PULL_UP)

DIR_PIN      = Pin(5, Pin.OUT,value =0)  # Richtungs-Pin 1 fährt runter!!!
STEP_PIN     = Pin(6, Pin.OUT,value =0)  # Schritt-Pin
SLEEP_PIN    = Pin(7, Pin.OUT,value =0)  # Aktivierung des Treibers
PSU24V       = Pin(12 , Pin.OUT, value=0)

micro_step_runter = 8		#1/8
micro_step_hoch   = 4		#1/4
ratio             = 30		
time_step_runter  = 1250 	       #in us
time_step_hoch 	  = 2500	#in us

grundpos=6 #in °

max_steps_hoch  = round((85/1.8)*micro_step_hoch*ratio)
max_steps_runter= round((85/1.8)*micro_step_runter*ratio)

def neigen_kali(NOTHALT):
    print("Referenzierung Neigen Achse")
    
    if ini_90geneigt.value()==0:
            #bereits in 90° Pos.
            return 0, 90
    else:
        PSU24V.value(1)
        sleep(1)      
        stepper.enable()
        stepper.setCurrent(3, 100)
        stepper.setStepMode(stepper.MicroStep4)
        DIR_PIN.value(0)    
        sleep(0.2)
        
    steps=0 
        
    while ini_90geneigt.value()==1 and  NOTHALT.locked()==False and max_steps_hoch>steps:
        STEP_PIN.value(1)
        sleep_us(round(time_step_hoch/2))
        STEP_PIN.value(0)
        sleep_us(round(time_step_hoch/2))
        steps+=1
    
    sleep(.2)
    stepper.disable()    
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
        print("Grundpos: %i° ist bereits angefahren!"%grundpos)
        return 0, grundpos
    
    print("Fahre Grundpos an!")
    
    #+3 grad damit Endlage safe angesprochen wird und Toleranzen ausgeglichen werden
    steps = round((pos+3-grundpos/1.8)*micro_step_runter*ratio) #Schritte berechnen
    
    DIR_PIN.value(1)
    PSU24V.value(1)
    sleep(.2)
    stepper.enable()
    stepper.setCurrent(3, 100)
    stepper.setStepMode(stepper.MicroStep8)
    
    for _ in range(steps):
        if NOTHALT.locked()== True:
            break
        STEP_PIN.value(1)
        sleep_us(round(time_step_runter/2)) 
        STEP_PIN.value(0)
        sleep_us(round(time_step_runter/2))
        if ini_0geneigt.value() == 0:
            print("Ini Grundpos geneigt betätigt")
            break
    
    sleep(.2)
    stepper.disable()
    PSU24V.value(0)
    
    if NOTHALT.locked()== True:
        print("Not-Halt hat ausgelöst")
        return 41,999
    
    if ini_0geneigt.value() == 0:
        return 0,grundpos
    else:
        print("hat Ini Grundpos nicht erreicht, muss von Hand angefahren werden")
        return 12,999


def neigen90(NOTHALT, pos):
    
    if ini_90geneigt.value() == 0:
        print("90° ist bereits angefahren!")
        return 0, 90
    
    print("Fahre 90° an!")

    #+3 grad damit Endlage safe angesprochen wird und Toleranzen ausgeglichen werden
    dif = 90 - pos
    steps = round((dif+3/1.8)*micro_step_hoch*ratio) #Schritte berechnen
    
    DIR_PIN.value(0)
    PSU24V.value(1)
    stepper.enable()
    stepper.setCurrent(3, 100)
    stepper.setStepMode(stepper.MicroStep4)
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
    stepper.disable()
    sleep(.2)
    PSU24V.value(0)
    
    if NOTHALT.locked()== True:
        print("Not-Halt hat ausgelöst")
        return 41,999
    
    if ini_90geneigt.value() == 0:
        return 0,90
    else:
        print("hat Ini 90° nicht erreicht, muss von Hand angefahren werden")
        return 11,999       
    
    
def neigen_sonne(NOTHALT, pos):

    print("Fahre Sonnenposition an!")
    print("Pos vor Fahrt: %i",pos)
    
    sonnen_pos = getSEA(51,7,2)
    print("Sonnenhöhe: %i"%sonnen_pos)
    if sonnen_pos < 0:
        print("die Sonne ist noch nicht aufgegangen")
        return 0,pos
    
    if sonnen_pos<grundpos:
        print("Sonenpos. kleiner Grundpos deshalb fahre auf Grundpos.")
        sonnen_pos = grundpos
    
    if sonnen_pos<=pos+1 and sonnen_pos>=pos-1:
        print("Steht noch +-1 in Sonnenposition")
        return 0,pos
    
    PSU24V.value(1)
    sleep(.2)
    stepper.enable()
    stepper.setCurrent(3, 100)
    
    if pos<sonnen_pos: #hoch fahren
        dif = sonnen_pos-pos
        steps = round((dif/1.8)*micro_step_hoch*ratio)
        DIR_PIN.value(0)
        stepper.setStepMode(stepper.MicroStep4)
        print("fahre hoch")
        time_step = time_step_hoch
        
    if pos>sonnen_pos: #runter fahren
        dif = pos-sonnen_pos
        print("Die differenz der pos. beträgt: %i"%dif)
        steps = round((dif/1.8)*micro_step_runter*ratio)    
        DIR_PIN.value(1)
        stepper.setStepMode(stepper.MicroStep8)
        print("fahre runter")
        time_step = time_step_runter  
    
    for _ in range(steps):
        if NOTHALT.locked()== True:
            break
        STEP_PIN.value(1)
        sleep_us(round(time_step/2)) 
        STEP_PIN.value(0)
        sleep_us(round(time_step/2))

        if ini_0geneigt.value() == 0 and DIR_PIN.value()==1 or ini_90geneigt.value() == 0 and DIR_PIN.value() == 0:
            print("Eine Endlage Neigen wurde betätigt")
            break
    
    stepper.disable()
    sleep(.2)
    PSU24V.value(0)
    
    if NOTHALT.locked()== True:
        print("Not-Halt hat ausgelöst")
        return 41,999
    
    if ini_90geneigt.value() == 0:
        return 10,90
    
    if ini_0geneigt.value() == 0 and sonnenpos<=grundpos+2: #+2 um Tolernaz auszugleichen
        return 0,grundpos
    
    if ini_0geneigt.value() == 0: #Fehlerhaft in Endlage gefahren
        return 10,grundpos
    
    return 0,sonnen_pos #wenn alles gut ist


def neigen_hand():
    
    while not(hoch.value()==0 and runter.value()==0):
        first_run_hoch   = True
        schleife_hoch    = False
        first_run_runter = True
        schleife_runter  = False        
        
        #Hoch Handbetrieb
        while hoch.value()==0 and ini_90geneigt.value()==1 and runter.value()==1:
            
            if first_run_hoch == True:
                first_run_hoch = False
                schleife_hoch = True

                DIR_PIN.value(0) 
                PSU24V.value(1)
                sleep(.3)
                stepper.enable()
                stepper.setCurrent(3, 100)
                stepper.setStepMode(stepper.MicroStep4)
                
                
            STEP_PIN.value(1)
            sleep_us(round(time_step_hoch/2)) 
            STEP_PIN.value(0)
            sleep_us(round(time_step_hoch/2))
            if ini_90geneigt.value() == 0:
                print("Ini 90° geneigt betätigt")
                sleep(.2)
                break
            
        if schleife_hoch == True:
            schleife_hoch = False
            stepper.disable()
            sleep(.1)
            PSU24V.value(0)

        
        #Runter Handbetrieb
        while runter.value()==0 and ini_0geneigt.value()==1 and hoch.value()==1:
            
            if first_run_runter == True:
                first_run_runter = False
                schleife_runter = True
                DIR_PIN.value(1) 
                PSU24V.value(1)
                sleep(.3)
                stepper.enable()
                stepper.setCurrent(3, 100)
                stepper.setStepMode(stepper.MicroStep8)
                
            STEP_PIN.value(1)
            sleep_us(round(time_step_runter/2)) 
            STEP_PIN.value(0)
            sleep_us(round(time_step_runter/2))
            if ini_0geneigt.value() == 0:
                print("Ini 0° geneigt betätigt")
                sleep(.2)
                break
            
        if schleife_runter == True:
            schleife_runter = False
            stepper.disable()
            sleep(.1)
            PSU24V.value(0)
        
#Endlage wieder hinzufügen!! Hand!        
#neigen_hand()         
#neigen90(NOTHALT,0)
#sleep(1)
#neigen_sonne(NOTHALT,90)
#sleep(5)
#neigen0(NOTHALT,90)
#neigen_sonne(NOTHALT,90)
#neigen_kali(NOTHALT)            
