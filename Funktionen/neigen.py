#ToDo: return false wenn endlage nicht erreicht wird

from machine import Pin
from time import sleep,sleep_us
from Sonne import getSEA

ini_0geneigt   = Pin(18 , Pin.IN,Pin.PULL_UP)
ini_90geneigt  = Pin(17 , Pin.IN,Pin.PULL_UP)

# Pins für den DRV8825 Schrittmotor-Treiber
DIR_PIN   = Pin(5, Pin.OUT,value =0)  # Richtungs-Pin 1 Uhrzeigersinn
STEP_PIN  = Pin(6, Pin.OUT,value =0)  # Schritt-Pin
SLEEP_PIN = Pin(7, Pin.OUT,value =0)  # Aktivierung des Treibers
PSU24V    = Pin(12 , Pin.OUT, value=0)

#1/4 Step:
# Mikroschritt-Modus 0 = 0
# Mikroschritt-Modus 1 = 1
# Mikroschritt-Modus 2 = 0

micro_step = 4 		#1/4
ratio      = 30		#gerade kein Getriebe am start
time_step  = 3000 	#in us

def neigen90():
    print("Fahre 90 grad an!")
    if ini_90geneigt.value()==0:
        print ("Bereits 90° geneigt")
        return(False)
    with open("tot_pos_neigen.txt","r") as datei:
        inhalt  = datei.read()
    pos = int(inhalt)
    print("aktuelle Pos. %i"%pos)
    dif = 90 - pos
    steps = round((dif/1.8)*micro_step*ratio) #Schritte berechnen
    gerade = steps%micro_step #für geringeren Schlag beim bestromen
    steps -= gerade
    DIR_PIN.value(1) #muss nach oben fahren! Muss überprüft werden
    PSU24V.value(1)    
    SLEEP_PIN.value(1)
    sleep(.1)
    
    for _ in range(steps):
        # Mache einen Schritt
        STEP_PIN.value(1)
        sleep_us(round(time_step/2))  # Wartezeit vor dem nächsten Schritt
        STEP_PIN.value(0)
        sleep_us(round(time_step/2))  # Wartezeit nach dem Schritt
        if ini_90geneigt.value() == 0:
            print ("Ini 90° geneigt angesprochen")
            break         
    sleep(.5)
    PSU24V.value(0)
    SLEEP_PIN.value(0)
    print("auf 90 grad geneigt")
    with open("tot_pos_neigen.txt","w") as datei:
            datei.write("90")
    sleep(1)

def neigen0():
    print("Fahre 0 grad an!")
    with open("tot_pos_neigen.txt","r") as datei:
        inhalt  = datei.read()
    pos = int(inhalt)
    print("aktuelle Pos. %i"%pos)
    steps = round((pos/1.8)*micro_step*ratio) #Schritte berechnen
    gerade = steps%micro_step #für geringeren Schlag beim bestromen
    steps -= gerade
    DIR_PIN.value(0) #muss nach unten fahren! Muss überprüft werden
    PSU24V.value(1)
    SLEEP_PIN.value(1)
    sleep(.1)
    for _ in range(steps):
        # Mache einen Schritt
        STEP_PIN.value(1)
        sleep_us(round(time_step/2))  # Wartezeit vor dem nächsten Schritt
        STEP_PIN.value(0)
        sleep_us(round(time_step/2))  # Wartezeit nach dem Schritt
        if ini_0geneigt.value() == 0:
            print("Ini 0° geneigt betätigt")
            break        
    sleep(.5)
    PSU24V.value(0)
    SLEEP_PIN.value(0)
    print("auf 0 grad geneigt")
    with open("tot_pos_neigen.txt","w") as datei:
            datei.write("0")    
    
    
def neigen_sonne():
    print("Fahre Sonnenhöhe an!")
    with open("tot_pos_neigen.txt","r") as datei:
        inhalt  = datei.read()
    pos = int(inhalt)
    print("ausgelesene Pos.: %i"%pos)
    sonnen_pos = getSEA(51,7,2)
    sonnen_pos = round(sonnen_pos)
    print("Sonnenhöhe: %i"%sonnen_pos)
    if sonnen_pos < 0:
        print("die Sonne ist noch nicht aufgegangen")
        return()
    dif= pos - sonnen_pos
    if dif==0:
        print("Steht noch im Sonnenwinkel!")
        return()
    if dif<0:
        DIR_PIN.value(1) #muss nach oben fahren ÜBERPRÜFEN
        neue_pos= pos + dif
        print("Fährt %i grad nach oben"%abs(dif))
        dif= abs(dif)
        
    else:
        DIR_PIN.value(0) #muss nach unten fahren ÜBERPRÜFEN
        neue_pos= pos - dif
        print("Fährt %i grad nach unten"%dif)
    SLEEP_PIN.value(1)
    PSU24V.value(1)
    sleep(.5)
    steps = round((dif/1.8)*micro_step*ratio)
    for _ in range(steps):
        # Mache einen Schritt
        STEP_PIN.value(1)
        sleep_us(round(time_step/2))  # Wartezeit vor dem nächsten Schritt
        STEP_PIN.value(0)
        sleep_us(round(time_step/2))  # Wartezeit nach dem Schritt
        if ini_90geneigt.value == 0 and DIR_PIN.value() == 1 or ini_0geneigt.value() == 0 and DIR_PIN.value() == 0:
            print("In Endlage gefahren!")
            break         
    sleep(.5)
    SLEEP_PIN.value(0)
    PSU24V.value(0)
    print ("auf %i grad geneigt!"%neue_pos)
    with open("tot_pos_neigen.txt","w") as datei:
        datei.write(str(neue_pos))
        
#neigen90()
#neigen0()
#neigen_sonne()
