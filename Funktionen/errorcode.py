from machine import I2C, Pin
from sh1106  import SH1106_I2C
i2c 	= I2C(0, scl=Pin(1), sda=Pin(0))
display	= SH1106_I2C(128, 64, i2c, Pin(28), 0x3c)

def fehlermeldung(fehler):
        if fehler == 10:
            print("Fehler re­fe­ren­zie­ren neigen")
            display.fill(0)
            display.text('Fehler'      , 0,  0, 1)
            display.text('re­fe­ren­zie­ren', 0, 10, 1)
            display.text('neigen'      , 0, 20, 1)
            display.show()
            return
        elif fehler == 11:
            print("Fehler aufneigen")
            display.fill(0)
            display.text('Fehler aufneigen', 0, 0, 1)
            display.show()
            return
        elif fehler == 12:
            print("Fehler zuneigen")
            display.fill(0)
            display.text('Fehler zuneigen', 0, 0, 1)
            display.show()
            return
        elif fehler == 20:
            print("Fehler re­fe­ren­zie­ren fächern")
            display.fill(0)
            display.text('Fehler'      , 0,  0, 1)
            display.text('re­fe­ren­zie­ren', 0, 10, 1)
            display.text('faechern'    , 0, 20, 1)
            display.show()
            return
        elif fehler == 21:
            print("Fehler auffächern")
            display.fill(0)
            display.text('Fehler'     , 0,  0, 1)
            display.text('auffaechern', 0, 10, 1)
            display.show()
            return
        elif fehler == 22:
            print("Fehler zufächern")
            display.fill(0)
            display.text('Fehler', 0,  0, 1)
            display.text('zufaechern', 0, 10, 1)
            display.show()
            return
        elif fehler == 30:
            print("Fehler re­fe­ren­zie­ren Drehen")
            display.fill(0)
            display.text('Fehler'      , 0,  0, 1)
            display.text('re­fe­ren­zie­ren', 0, 10, 1)
            display.text('drehen'      , 0, 20, 1)
            display.show()
            return
        elif fehler == 31:
            print("Fehler drehen")
            display.fill(0)
            display.text('Fehler drehen', 0, 0, 1)
            display.show()
            return
        elif fehler == 41:
            print("Nothalt ausgelöst!")
            display.fill(0)
            display.text('Nothalt'       , 0,  0, 1)
            display.text('betaetigt!'    , 0, 10, 1)
            display.text('Zum quittieren', 0, 20, 1)
            display.text('2x Start'      , 0, 30, 1)
            display.text('druecken.'     , 0, 40, 1)
            display.show()
            return
