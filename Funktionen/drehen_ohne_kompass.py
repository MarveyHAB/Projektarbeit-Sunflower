from machine    import Pin
from time       import sleep_us,sleep,sleep_ms
#from hmc5883l import HMC5883L
from Sonne      import getAZ

ini_grund_pos= Pin(16 , Pin.IN,Pin.PULL_UP)
brake     = Pin(11 , Pin.OUT,value =0)
rechts   = Pin(22 , Pin.IN,Pin.PULL_UP)
links   = Pin(27 , Pin.IN,Pin.PULL_UP)

# Pins für den DRV8825 Schrittmotor-Treiber
DIR_PIN   = Pin(2, Pin.OUT,value =0)  # Richtungs-Pin 1 Uhrzeigersinn
STEP_PIN  = Pin(3, Pin.OUT,value =0)  # Schritt-Pin
SLEEP_PIN = Pin(4, Pin.OUT,value =0)  # Aktivierung des Treibers
PSU_24V   = Pin (12, Pin.OUT,value =0)#24 aktivieren

micro_step = 4 		#1/4
ratio      = 50		#gerade kein Getriebe am start
time_step  =2500 	#in us
grund_pos = 180


#fehler 30 Kalibrieren
def drehen_kali(NOTHALT):
    if ini_grund_pos.value() == 0:
            print ("Ini Drehen Grundpos. angesprochen")
            with open("totale_pos.txt","r") as datei:
                inhalt  = datei.read()
                abs_pos = int(inhalt)
            if abs_pos != 180:
                with open("totale_pos.txt","w") as datei:
                    datei.write("180")
            return 0,180

    with open("totale_pos.txt","r") as datei:
        inhalt  = datei.read()
        abs_pos = int(inhalt)
    
    if abs_pos<180: #dann rechts fahren
        DIR_PIN.value(0) #im Uhrzeigersinn
        dif= 180-abs_pos
    
    if abs_pos>180: #dann links fahren
        DIR_PIN.value(1)
        dif= abs_pos-180
        
    PSU_24V.value(1)
    SLEEP_PIN.value(1)
    brake.value(1)
    sleep(.2)
    ini_angesprochen = False
    
    #Nothalt einfügen
    #und falls zu viele schritte gemacht werden
    for _ in range(steps):
        if NOTHALT.locked()== True:
            break
        STEP_PIN.value(1)
        sleep_us(round(time_step/2))  # Wartezeit vor dem nächsten Schritt
        STEP_PIN.value(0)
        sleep_us(round(time_step/2))  # Wartezeit nach dem Schritt
        if ini_grund_pos.value() == 0:
            print ("Ini Drehen Grundpos. angesprochen")
            break
        
        if NOTHALT.locked()== True:
        print("Not-Halt hat ausgelöst")
        return 41,999
        
        with open("totale_pos.txt","w") as datei:
            datei.write("180")
        
        if ini_grund_pos.value() == 0:
        return 0,180
        else:
            print("Muss im Handbetrieb angefahren werden, da er die pos. nicht findet.")
            return 30,180
        
        
def drehen_hand(NOTHALT):
    while rechts.value()==1 or links.value()==1:
        
        first_run_rechts   = True
        schleife_rechts    = False
        first_run_links = True
        schleife_links  = False        
        
        #rechts Handbetrieb
        while rechts.value()==0 and links.value()==1:
            
            if NOTHALT.locked()== True:
                break
            
            if first_run_rechts == True:
                first_run_rechts = False
                schleife_rechts = True
                DIR_PIN.value(1) 
                PSU24V.value(1)
                SLEEP_PIN.value(1)
                sleep(.2)
                
            STEP_PIN.value(1)
            sleep_us(round(time_step/2)) 
            STEP_PIN.value(0)
            sleep_us(round(time_step/2))
            
        if schleife_rechts == True:
            schleife_rechts = False
            sleep(.1)
            PSU24V.value(0)
            SLEEP_PIN.value(0)
            sleep(.2)
        
        #links Handbetrieb
        while links.value()==0 and rechts.value()==1:
            
            if NOTHALT.locked()== True:
                break
            
            if first_run_links == True:
                first_run_links = False
                schleife_links = True
                DIR_PIN.value(0) 
                PSU24V.value(1)
                SLEEP_PIN.value(1)
                sleep(.2)
                
            STEP_PIN.value(1)
            sleep_us(round(time_step/2)) 
            STEP_PIN.value(0)
            sleep_us(round(time_step/2))
            
        if schleife_links == True:
            schleife_links = False
            sleep(.1)
            PSU24V.value(0)
            SLEEP_PIN.value(0)
            sleep(.2)


def drehen_grundpos(NOTHALT,pos):
    PSU_24V.value(1)
#aktuelle Position herausfinden
    with open("totale_pos.txt","r") as datei:
        inhalt  = datei.read()
        abs_pos = int(inhalt)
    akt_pos = abs_pos
    print("aktuelle Pos.:%i"%akt_pos)
    if akt_pos == grund_pos:
        print("aktuelle Pos. entspricht noch der Grundpos.")
        return 0,pos
# Berechnung des kürzesten Weges im Uhrzeigersinn
    im_uhrzeigersinn = (grund_pos - akt_pos) % 360
# Berechnung des kürzesten Weges gegen den Uhrzeigersinn
    gegen_uhrzeigersinn = (akt_pos - grund_pos) % 360
#was ist kürzer
    if im_uhrzeigersinn<gegen_uhrzeigersinn:
        DIR_PIN.value(0) #im Uhrzeigersinn
        print("im Uhrzeigersinn sind es %i grad"%im_uhrzeigersinn)
        dif=im_uhrzeigersinn
        if 360<akt_pos+dif:
            akt_pos=akt_pos-360+dif
        else:
            akt_pos=akt_pos+dif
    else:
        DIR_PIN.value(1) #gegen den Uhrzeigersinn
        print("gegen Uhrzeigersinn sind es %i grad"%gegen_uhrzeigersinn)
        dif=gegen_uhrzeigersinn
        if 0>akt_pos-dif:
            akt_pos=akt_pos+360-dif
        else:
            akt_pos=akt_pos-dif
    #+5° damit er den Ini auf jeden Fall erreicht, wenn nicht liegt vermutlich ein Fehler vor
    steps = round(((dif+5)/1.8)*micro_step*ratio)
    # Schalte den Treiber ein
    SLEEP_PIN.value(1)
    sleep(.2)
    brake.value(1)
    sleep(.2)
    ini_angesprochen = False
    for _ in range(steps):
        # Mache einen Schritt
        STEP_PIN.value(1)
        sleep_us(round(time_step/2))  # Wartezeit vor dem nächsten Schritt
        STEP_PIN.value(0)
        sleep_us(round(time_step/2))  # Wartezeit nach dem Schritt
        if ini_grund_pos.value() == 0:
            print ("Ini Drehen Grundpos. angesprochen")
            ini_angesprochen = True
            break
    brake.value(0)
    sleep(.2)
    SLEEP_PIN.value(0)
    print("angefahrene Pos. %i"%akt_pos)
    with open("totale_pos.txt","w") as datei:
            datei.write(str(akt_pos))
    if ini_angesprochen == False:
        print("Ini Grundpos. wurde nicht erreicht")
        return 31,180 #anpassen
    PSU_24V.value(0)


def drehen_sonne(NOTHALT,pos):
    PSU_24V.value(1)
#aktuelle Sonnenposition abfragen
    sunPos = int(getAZ(51,7,2))
    print("Sonnenposition: %i"%sunPos)
#aktuelle Position herausfinden
    with open("totale_pos.txt","r") as datei:
        inhalt  = datei.read()
        abs_pos = int(inhalt)
    akt_pos = abs_pos
    print("aktuelle Pos.:%i"%akt_pos)
    if akt_pos == sunPos:
        print("aktuelle Pos. entspricht noh der Sonnenpos.")
        return(0,pos)
# Berechnung des kürzesten Weges im Uhrzeigersinn
    im_uhrzeigersinn = (sunPos - akt_pos) % 360
# Berechnung des kürzesten Weges gegen den Uhrzeigersinn
    gegen_uhrzeigersinn = (akt_pos - sunPos) % 360
#was ist kürzer
    if im_uhrzeigersinn<gegen_uhrzeigersinn:
        DIR_PIN.value(0) #im Uhrzeigersinn
        print("im Uhrzeigersinn sind es %i grad"%im_uhrzeigersinn)
        dif=im_uhrzeigersinn
        if 360<akt_pos+dif:
            akt_pos=akt_pos-360+dif
        else:
            akt_pos=akt_pos+dif
    else:
        DIR_PIN.value(1) #gegen den Uhrzeigersinn
        print("gegen Uhrzeigersinn sind es %i grad"%gegen_uhrzeigersinn)
        dif=gegen_uhrzeigersinn
        if 0>akt_pos-dif:
            akt_pos=akt_pos+360-dif
        else:
            akt_pos=akt_pos-dif
    #getriebeübersetzug 1/30 und 1/4 multistepping
    steps = round((dif/1.8)*micro_step*ratio)
    # Schalte den Treiber ein
    SLEEP_PIN.value(1)
    sleep(.2)
    brake.value(1)
    sleep(.5)
    for _ in range(steps):
        # Mache einen Schritt
        STEP_PIN.value(1)
        sleep_us(round(time_step/2))  # Wartezeit vor dem nächsten Schritt
        STEP_PIN.value(0)
        sleep_us(round(time_step/2))  # Wartezeit nach dem Schritt
    brake.value(0)
    sleep(.2)
    SLEEP_PIN.value(0)
    print("angefahrene Pos. %i"%akt_pos)
    with open("totale_pos.txt","w") as datei:
            datei.write(str(akt_pos))
    PSU_24V.value(0)
    return 0,akt_pos

#drehen_sonne()
#drehen_grundpos()


