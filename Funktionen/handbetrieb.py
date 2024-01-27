from drehen import drehen_hand
from neigen import neigen_hand
from faechern import faechern_hand
from sh1106 	import SH1106_I2C
from machine import I2C, Pin

i2c 	= I2C(0, scl=Pin(1), sda=Pin(0))
display	= SH1106_I2C(128, 64, i2c, Pin(28), 0x3c)

while True:
    display.sleep(False)
    display.fill(0)
    display.text('Sunflower ', 30, 20, 1)
    display.text('Handbetrieb'   , 20, 30, 1)
    display.show()
    print("Wähle eine Hand-Funktion:")
    print("1. Drehen")
    print("2. Neigen")
    print("3. Fächern")
    print("Q. Beenden")
    print("Um zum Menü zurückzukehren, drücke beide Tasten gleichzeitig")
    
    # Benutzereingabe erfassen
    eingabe = input("Deine Auswahl: ")

    # Funktion basierend auf der Eingabe aufrufen
    if eingabe.lower() == '1':
        drehen_hand()
    elif eingabe.lower() == '2':
        neigen_hand()
    elif eingabe.lower() == '3':
        faechern_hand()
    elif eingabe.lower() == 'q':
        print("Programm beendet.")
        break
    else:
        print("Ungültige Auswahl. Versuche es erneut.")