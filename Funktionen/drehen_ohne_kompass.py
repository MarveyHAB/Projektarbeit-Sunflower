from machine import Pin
from time import sleep_us,sleep,sleep_ms
from hmc5883l import HMC5883L

brake     = Pin(11 , Pin.OUT,value =0)
# Pins für den DRV8825 Schrittmotor-Treiber
DIR_PIN   = Pin(2, Pin.OUT,value =0)  # Richtungs-Pin 1 Uhrzeigersinn
STEP_PIN  = Pin(3, Pin.OUT,value =0)  # Schritt-Pin
SLEEP_PIN = Pin(4, Pin.OUT,value =0)  # Aktivierung des Treibers
#1/4 Step:
# Mikroschritt-Modus 0 = 0
# Mikroschritt-Modus 1 = 1
# Mikroschritt-Modus 2 = 0



def step(sunPos):
        with open("totale_pos.txt","r") as datei:
            inhalt  = datei.read()
            abs_pos = int(inhalt)
        akt_pos = abs_pos
        #Winkeldifferenz
        dif= abs(akt_pos-sunPos)
        print(dif)
        #rechts oder links
        if dif>180:
            dif = 360 - dif
            DIR_PIN.value(0)
            print("es wird %i grad gegen den Uhrzeigersinn gefahren"%dif)
            if 0>akt_pos-dif:
                akt_pos=akt_pos+360-dif
            else:
                akt_pos=akt_pos-dif
        else:
            DIR_PIN.value(1)
            print("es wird %i grad im Uhrzeigersinn gefahren"%dif)
            if 360<akt_pos+dif:
                akt_pos=akt_pos-360+dif
            else:
                akt_pos=akt_pos+dif
        print(dif)
        #getriebeübersetzug 1/30 und 1/4 multistepping
        steps = int(dif/(1.8/(4*30)))
        # Schalte den Treiber ein
        SLEEP_PIN.value(1)
        sleep(1)
        for _ in range(steps):
            # Mache einen Schritt
            STEP_PIN.value(1)
            sleep_us(1000)  # Wartezeit vor dem nächsten Schritt
            STEP_PIN.value(0)
            sleep_us(1000)  # Wartezeit nach dem Schritt
        sleep_ms(500)
        SLEEP_PIN.value(0)
        print("angefahrene Pos. %i"%abs_pos)
        '''
        with open("totale_pos.txt","w") as datei:
                datei.write(abs_pos)
        '''
step(320)

    





