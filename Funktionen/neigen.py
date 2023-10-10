from machine import Pin
from time import sleep,sleep_us
from Sonne import getSEA

ini_0geneigt   = Pin(18 , Pin.IN,Pin.PULL_DOWN)
ini_90geneigt  = Pin(19 , Pin.IN,Pin.PULL_DOWN)
brake     = Pin(12 , Pin.OUT,value =0)
# Pins für den DRV8825 Schrittmotor-Treiber
DIR_PIN   = Pin(5, Pin.OUT,value =0)  # Richtungs-Pin 1 Uhrzeigersinn
STEP_PIN  = Pin(6, Pin.OUT,value =0)  # Schritt-Pin
SLEEP_PIN = Pin(7, Pin.OUT,value =0)  # Aktivierung des Treibers
#1/4 Step:
# Mikroschritt-Modus 0 = 0
# Mikroschritt-Modus 1 = 1
# Mikroschritt-Modus 2 = 0

def neigen90():
    print("Fahre 90 grad an!")
    if ini_0geneigt==0:
        print ("Unbestimmte Pos")
        return(False)
    steps = round(90/(1.8/(4*30)))
    DIR_PIN.value(1) #muss nach oben fahren! Muss überprüft werden
    SLEEP_PIN.value(1)
    sleep(.5)
    brake.value(1)
    sleep(.5)
    for _ in range(steps):
        # Mache einen Schritt
        STEP_PIN.value(1)
        sleep_us(500)  # Wartezeit vor dem nächsten Schritt
        STEP_PIN.value(0)
        sleep_us(500)  # Wartezeit nach dem Schritt
        if ini_90geneigt == 1:
            break         
    brake.value(0)
    sleep(.5)
    SLEEP_PIN.value(0)
    print("auf 90 grad geneigt")
    with open("tot_pos_neigen.txt","w") as datei:
            datei.write("90")    

def neigen0():
    print("Fahre 0 grad an!")
    with open("tot_pos_neigen.txt","r") as datei:
        inhalt  = datei.read()
    pos = int(inhalt)
    steps = round(pos/(1.8/(4*30))) #Schritte berechnen
    DIR_PIN.value(1) #muss nach unten fahren! Muss überprüft werden
    SLEEP_PIN.value(1)
    sleep(.5)
    brake.value(1)
    sleep(.5)
    for _ in range(steps):
        # Mache einen Schritt
        STEP_PIN.value(1)
        sleep_us(500)  # Wartezeit vor dem nächsten Schritt
        STEP_PIN.value(0)
        sleep_us(500)  # Wartezeit nach dem Schritt
        if ini_0geneigt == 1:
            break         
    brake.value(0)
    sleep(.5)
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
    sleep(.5)
    brake.value(1)
    sleep(.5)
    steps = round(dif/(1.8/(4*30)))
    for _ in range(steps):
        # Mache einen Schritt
        STEP_PIN.value(1)
        sleep_us(500)  # Wartezeit vor dem nächsten Schritt
        STEP_PIN.value(0)
        sleep_us(500)  # Wartezeit nach dem Schritt
        if ini_90geneigt == 1 and DIR_PIN == 1 or ini_0geneigt == 1 and DIR_PIN == 0:
            print("In Endlage gefahren!")
            break         
    brake.value(0)
    sleep(.5)
    SLEEP_PIN.value(0)
    print ("auf %i grad geneigt!"%neue_pos)
    with open("tot_pos_neigen.txt","w") as datei:
        datei.write(str(neue_pos))



