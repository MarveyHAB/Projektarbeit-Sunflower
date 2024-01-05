from machine import Pin
from time import sleep,sleep_us

ini_eingefaechert = Pin(20 , Pin.IN,Pin.PULL_UP)
ini_ausgefaechert = Pin(19 , Pin.IN,Pin.PULL_UP)
# Pins für den DRV8825 Schrittmotor-Treiber
DIR_PIN   = Pin(8 , Pin.OUT,value =0)  # Richtungs-Pin 1 Uhrzeigersinn
STEP_PIN  = Pin(9 , Pin.OUT,value =0)  # Schritt-Pin
SLEEP_PIN = Pin(10, Pin.OUT,value =0)  # Aktivierung des Treibers
PSU24V = Pin(12 , Pin.OUT, value=0)

#1/4 Step:
# Mikroschritt-Modus 0 = 0
# Mikroschritt-Modus 1 = 1
# Mikroschritt-Modus 2 = 0
micro_step = 4 #1/4
ratio      = 30
time_step  = 1500

def auffaechern():
    print("wird aufgefaechert")
    if ini_eingefaechert.value()==1:
        print ("Unbestimmte Pos und wird deswegen doch nicht aufgefächert")
        return(False)
    
    DIR_PIN.value(1) #überprüfen
    steps = round((360/1.8)*micro_step*ratio)
    print("360grad sind %i steps"%steps)
    print("einfahren dauert %i s"%(int(steps* time_step*0.000001)))
    # Schalte den Treiber ein
    SLEEP_PIN.value(1)
    PSU24V.value(1)
    sleep(.5)
    for _ in range(steps):
        # Mache einen Schritt
        STEP_PIN.value(1)
        sleep_us(int(time_step/2))  # Wartezeit vor dem nächsten Schritt
        STEP_PIN.value(0)
        sleep_us(int(time_step/2))  # Wartezeit nach dem Schritt
        if ini_ausgefaechert.value() == 0:
            print ("Ini ausgefächert angesprochen")
            break
            #bzw nur noch ein paar schritte
    sleep(0.5)
    SLEEP_PIN.value(0)
    PSU24V.value(0)
    print("aufgefaechert")
    
def einfaechern():
    print("wird eingefaechert")
    if ini_ausgefaechert.value()==1:
        print ("Unbestimmte Pos und wird deswegen doch nicht aufgefächert")
        return(False)
    
    DIR_PIN.value(0) #überprüfen
    steps = round((360/1.8)*micro_step*ratio)
    print("360grad sind %i steps"%steps)
    print("einfahren dauert %i s"%(int(steps* time_step*0.000001)))
    # Schalte den Treiber ein
    SLEEP_PIN.value(1)
    PSU24V.value(1)
    sleep(.5)
    for _ in range(steps):
        # Mache einen Schritt
        STEP_PIN.value(1)
        sleep_us(int(time_step/2))  # Wartezeit vor dem nächsten Schritt
        STEP_PIN.value(0)
        sleep_us(int(time_step/2))  # Wartezeit nach dem Schritt
        if ini_eingefaechert.value() == 0:
            break
            #bzw nur noch ein paar schritte
    sleep(0.5)
    SLEEP_PIN.value(0)
    PSU24V.value(0)
    print("eingefaechert")        



