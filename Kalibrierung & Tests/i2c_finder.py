from machine import I2C, Pin, Timer
from sys import exit

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
print (i2c)
geraeteliste = i2c.scan()
if (len(geraeteliste)==0):
    print ("kein gerät gefunden!")
    exit()
for x in range(len(geraeteliste)):
    print ("I2C Teilnehmer Adresse: %i"%geraeteliste[x])
    print(hex(geraeteliste[x]))
