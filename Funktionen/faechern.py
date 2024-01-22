#ToDo: return false wenn endlage nicht erreicht wird

from machine import Pin
from time import sleep,sleep_us

ini_eingefaechert = Pin(20 , Pin.IN,Pin.PULL_UP)
ini_ausgefaechert = Pin(19 , Pin.IN,Pin.PULL_UP)
auf               = Pin(26 , Pin.IN,Pin.PULL_UP)
zu                = Pin(27 , Pin.IN,Pin.PULL_UP)
# Pins für den DRV8825 Schrittmotor-Treiber
DIR_PIN   = Pin(8 , Pin.OUT,value =0)  # 1 = Zufächern 0= Auffächern
STEP_PIN  = Pin(9 , Pin.OUT,value =0)  # Schritt-Pin
SLEEP_PIN = Pin(10, Pin.OUT,value =0)  # Aktivierung des Treibers
PSU24V = Pin(12 , Pin.OUT, value=0)

#muss 315° fächern

micro_step = 4 #1/4
ratio      = 30
time_step  = 1500


def faechern_kali(NOTHALT):
    return 0 #weil fächern nicht getestet werden kann
    print("wird aufgefaechert")
    
    if ini_ausgefaechert.value() == 0:
        print("Ist aufgefächert!")
        return 0
    
    steps = round((318/1.8)*micro_step*ratio)# Eigentlich 315° Fächern +3 für Toleranz
    
    DIR_PIN.value(0)
    SLEEP_PIN.value(1)
    PSU24V.value(1)
    sleep(.5)
    steps=500 #wieder rausnehmen mit inis
    
    for _ in range(steps):
        if NOTHALT.locked()== True:
            break
        STEP_PIN.value(1)
        sleep_us(int(time_step/2))
        STEP_PIN.value(0)
        sleep_us(int(time_step/2))
        if ini_ausgefaechert.value() == 0:
            print ("Ini ausgefächert angesprochen")
            break
            #bzw nur noch ein paar schritte
    sleep(.5)
    SLEEP_PIN.value(0)
    PSU24V.value(0)
    
    if NOTHALT.locked()== True:
        print("Not-Halt hat ausgelöst")
        return 41
    
    if ini_ausgefaechert.value() == 1:
        print("Ini ist nicht angesprochen, Kalibirierung fehlgeschlagen!")
        return 20
    
    print("Kalibrierung fächern erfolgreich")
    return 0  


def auffaechern(NOTHALT):
    return 0 #weil fächern nicht getestet werden kann
    print("wird aufgefaechert")
    
    steps = round((318/1.8)*micro_step*ratio)# Eigentlich 315° Fächern +3 für Toleranz
    
    DIR_PIN.value(0)
    SLEEP_PIN.value(1)
    PSU24V.value(1)
    sleep(.5)
    steps=500 #wieder rausnehmen mit inis
    
    for _ in range(steps):
        if NOTHALT.locked()== True:
            break
        STEP_PIN.value(1)
        sleep_us(int(time_step/2))
        STEP_PIN.value(0)
        sleep_us(int(time_step/2))
        if ini_ausgefaechert.value() == 0:
            print ("Ini ausgefächert angesprochen")
            break
            #bzw nur noch ein paar schritte
    sleep(.5)
    SLEEP_PIN.value(0)
    PSU24V.value(0)
    
    if NOTHALT.locked()== True:
        print("Not-Halt hat ausgelöst")
        return 41
    
    if ini_ausgefaechert.value() == 1:
        print("Ini ist nicht angesprochen, muss von Hand angefahren werden!")
        return 21
    
    return 0
    

def einfaechern(NOTHALT):
    return 0 #weil fächern nicht getestet werden kann
    print("wird eingefaechert")
    
    DIR_PIN.value(1)
    steps = round((318/1.8)*micro_step*ratio) # Eigentlich 315° Fächern +3 für Toleranz
    
    SLEEP_PIN.value(1)
    PSU24V.value(1)
    sleep(.5)
    steps=150 #noch loeschen
    for _ in range(steps):
        if NOTHALT.locked()== True:
            break
        STEP_PIN.value(1)
        sleep_us(int(time_step/2))
        STEP_PIN.value(0)
        sleep_us(int(time_step/2))
        if ini_eingefaechert.value() == 0:
            break
            #bzw nur noch ein paar schritte
    sleep(.5)
    SLEEP_PIN.value(0)
    PSU24V.value(0)
    
    if NOTHALT.locked()== True:
        print("Not-Halt hat ausgelöst")
        return 41
    
    if ini_eingefaechert.value() == 1:
        print("Ini ist nicht angesprochen, muss von Hand angefahren werden!")
        return 22
    
    print("eingefaechert")
    
    return 0


def faechern_hand():
    
    while auf.value()==1 or zu.value()==1:
        
        first_run_auf   = True
        schleife_auf    = False
        first_run_zu    = True
        schleife_zu     = False        
        
        #auf Handbetrieb
        while auf.value()==0 and ini_ausgefaechert.value()==1 and zu.value()==1:
            
            if NOTHALT.locked()== True:
                break
            
            if first_run_auf == True:
                first_run_auf = False
                print("auf fächern")
                schleife_auf = True
                DIR_PIN.value(0) 
                PSU24V.value(1)
                SLEEP_PIN.value(1)
                sleep(.2)
                
            STEP_PIN.value(1)
            sleep_us(round(time_step/2)) 
            STEP_PIN.value(0)
            sleep_us(round(time_step/2))
            if ini_ausgefaechert.value() == 0:
                print("Ini aufgefaechert betätigt")
                break
            
        if schleife_auf == True:
            schleife_auf = False
            sleep(.1)
            PSU24V.value(0)
            SLEEP_PIN.value(0)
            sleep(.2)
        
        #zu Handbetrieb
        while zu.value()==0 and ini_eingefaechert.value()==1 and auf.value()==1:
            
            if NOTHALT.locked()== True:
                break
            
            if first_run_zu == True:
                first_run_zu = False
                print("zu fächern")
                schleife_zu = True
                DIR_PIN.value(1) 
                PSU24V.value(1)
                SLEEP_PIN.value(1)
                sleep(.2)
                
            STEP_PIN.value(1)
            sleep_us(round(time_step/2)) 
            STEP_PIN.value(0)
            sleep_us(round(time_step/2))
            if ini_eingefaechert.value() == 0:
                print("Ini 0° eingefächert betätigt")
                break
            
        if schleife_zu == True:
            schleife_zu = False
            sleep(.1)
            PSU24V.value(0)
            SLEEP_PIN.value(0)
            sleep(.2)
    return 0    
    
#einfaechern(NOTHALT)
#auffaechern(NOTHALT)
#faechern_hand()


