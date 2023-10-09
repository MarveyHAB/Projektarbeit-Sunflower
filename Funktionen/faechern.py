brake     = Pin(13 , Pin.OUT,value =0)
# Pins für den DRV8825 Schrittmotor-Treiber
DIR_PIN   = Pin(8 , Pin.OUT,value =0)  # Richtungs-Pin 1 Uhrzeigersinn
STEP_PIN  = Pin(9 , Pin.OUT,value =0)  # Schritt-Pin
SLEEP_PIN = Pin(10, Pin.OUT,value =1)  # Aktivierung des Treibers
#1/4 Step:
# Mikroschritt-Modus 0 = 0
# Mikroschritt-Modus 1 = 1
# Mikroschritt-Modus 2 = 0
