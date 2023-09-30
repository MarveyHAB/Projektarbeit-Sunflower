from machine import Pin
from time import sleep_us,sleep,sleep_ms
from hmc5883l import HMC5883L

# Pins für den DRV8825 Schrittmotor-Treiber
ENABLE_PIN = Pin(11, Pin.OUT,value =1)  # Aktivierung des Treibers
DIR_PIN = Pin(12, Pin.OUT,value =0)  # Richtungs-Pin 1 Uhrzeigersinn
STEP_PIN = Pin(13, Pin.OUT,value =0)  # Schritt-Pin
#1/4 Step:
MODE0_PIN = Pin(16, Pin.OUT,value =0)  # Mikroschritt-Modus 0
MODE1_PIN = Pin(17, Pin.OUT,value =1)  # Mikroschritt-Modus 1
MODE2_PIN = Pin(18, Pin.OUT,value =0)  # Mikroschritt-Modus 2


def step(sunPos):
    #Berechnung für kürzesten Weg
    magnetometer = HMC5883L()
    #durchgang 0 grob anfahrt auf 70%
    #durchgang 1 kontrolliert die position nochmal und fährt korrigierten wert auf 90%
    #durchgang 2 kontrolliert die position nochmal und fährt korrigierten wert an
    durchgang=0
    while durchgang<3:
        x, y, z = magnetometer.read()
        aktPos, minutes = magnetometer.heading(x, y)
        print("Pos. vor Durchgang %i: %i"%(durchgang,aktPos))
        dif=aktPos-sunPos
        if (dif>-180 and (dif<0))or dif>180:#mit dem uhrzeigersinn
            DIR_PIN.value(1)
        else:
            DIR_PIN.value(0)
        if dif>180:
            dif=360-dif
        print("so viel grad %i wird gefahren"%abs(dif))
        #bei kurzer Fahrt reicht ein durchgang
        if abs(dif)<10:
            durchgang=3
        #getriebeübersetzug 1/30 und 1/4 multistepping
        steps = int(abs(dif)/(1.8/(4*30)))
        if durchgang==0:
            steps=int(steps*0.7)
        if durchgang==1:
            steps=int(steps*0.9)
        # Schalte den Schrittmotor ein
        ENABLE_PIN.value(0)
        for _ in range(steps):
            # Mache einen Schritt
            STEP_PIN.value(1)
            sleep_us(500)  # Wartezeit vor dem nächsten Schritt
            STEP_PIN.value(0)
            sleep_us(500)  # Wartezeit nach dem Schritt
        durchgang=durchgang+1
        sleep_ms(500)
    ENABLE_PIN.value(1)
    x, y, z = magnetometer.read()
    aktPos, minutes = magnetometer.heading(x, y)
    print("angefahrene Pos. %i"%aktPos)


    


