from machine import Pin
from time import sleep

ini_eingefaechert = Pin(20 , Pin.IN,Pin.PULL_DOWN)
ini_ausgefaechert = Pin(21 , Pin.IN,Pin.PULL_DOWN)
brake     = Pin(13 , Pin.OUT,value =0)
# Pins für den DRV8825 Schrittmotor-Treiber
DIR_PIN   = Pin(8 , Pin.OUT,value =0)  # Richtungs-Pin 1 Uhrzeigersinn
STEP_PIN  = Pin(9 , Pin.OUT,value =0)  # Schritt-Pin
SLEEP_PIN = Pin(10, Pin.OUT,value =1)  # Aktivierung des Treibers
#1/4 Step:
# Mikroschritt-Modus 0 = 0
# Mikroschritt-Modus 1 = 1
# Mikroschritt-Modus 2 = 0

def auffaechern():
    if ini_eingefaechert==0:
        print ("Unbestimmte Pos")
        return(False)
    DIR_PIN.value(1) #überprüfen
    steps = int(360/(1.8/(4*30)))
    # Schalte den Treiber ein
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
        if ini_ausgefaechert == 1:
            break 
    brake.value(0)
    sleep(0.5)
    SLEEP_PIN.value(0)
    
def einfaechern():
    if ini_ausgefaechert==0:
        print ("Unbestimmte Pos")
        return(False)
    DIR_PIN.value(0) #überprüfen
    steps = int(360/(1.8/(4*30)))
    # Schalte den Treiber ein
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
        if ini_eingefaechert == 1:
            break 
    brake.value(0)
    sleep(.5)
    SLEEP_PIN.value(0)
        

