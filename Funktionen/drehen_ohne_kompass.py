from machine import Pin
from time import sleep_us,sleep,sleep_ms
from hmc5883l import HMC5883L
from Sonne import getAZ

brake     = Pin(11 , Pin.OUT,value =0)
# Pins für den DRV8825 Schrittmotor-Treiber
DIR_PIN   = Pin(2, Pin.OUT,value =0)  # Richtungs-Pin 1 Uhrzeigersinn
STEP_PIN  = Pin(3, Pin.OUT,value =0)  # Schritt-Pin
SLEEP_PIN = Pin(4, Pin.OUT,value =0)  # Aktivierung des Treibers
#1/4 Step:
# Mikroschritt-Modus 0 = 0
# Mikroschritt-Modus 1 = 1
# Mikroschritt-Modus 2 = 0

def step():
    #aktuelle Sonnenposition abfragen
        sunPos = int(getAZ(51,7,2))
    #aktuelle Position herausfinden
        with open("totale_pos.txt","r") as datei:
            inhalt  = datei.read()
            abs_pos = int(inhalt)
        akt_pos = abs_pos
        print("Sonnenposition: %i"%sunPos)
        print("aktuelle Pos.:%i"%akt_pos)   
    # Berechnung des kürzesten Weges im Uhrzeigersinn
        im_uhrzeigersinn = (sunPos - akt_pos) % 360
    # Berechnung des kürzesten Weges gegen den Uhrzeigersinn
        gegen_uhrzeigersinn = (akt_pos - sunPos) % 360
    #was ist kürzer
        if im_uhrzeigersinn<gegen_uhrzeigersinn:
            DIR_PIN.value(1) #im Uhrzeigersinn
            print("im Uhrzeigersinn sind es %i grad"%im_uhrzeigersinn)
            dif=im_uhrzeigersinn
            if 360<akt_pos+dif:
                akt_pos=akt_pos-360+dif
            else:
                akt_pos=akt_pos+dif
        else:
            DIR_PIN.value(0) #gegen den Uhrzeigersinn
            print("gegen Uhrzeigersinn sind es %i grad"%gegen_uhrzeigersinn)
            dif=gegen_uhrzeigersinn
            if 0>akt_pos-dif:
                akt_pos=akt_pos+360-dif
            else:
                akt_pos=akt_pos-dif
        #getriebeübersetzug 1/30 und 1/4 multistepping
        steps = int(dif/(1.8/(4*30)))
        # Schalte den Treiber ein
        SLEEP_PIN.value(1)
        sleep(1)
        for _ in range(steps):
            # Mache einen Schritt
            STEP_PIN.value(1)
            sleep_us(500)  # Wartezeit vor dem nächsten Schritt
            STEP_PIN.value(0)
            sleep_us(500)  # Wartezeit nach dem Schritt
        sleep_ms(500)
        SLEEP_PIN.value(0)
        print("angefahrene Pos. %i"%akt_pos)
        with open("totale_pos.txt","w") as datei:
                datei.write(str(akt_pos))
step()
