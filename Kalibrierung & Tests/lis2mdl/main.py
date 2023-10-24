import lm75a
import math
from machine import Pin, I2C
from time import sleep_ms
from lis2mdl import LIS2MDL

i2c = I2C(0, sda=Pin(4), scl=Pin(5))  # Correct I2C pins for RP2040
lis = LIS2MDL(i2c)

while True:
    mag_x, mag_y, mag_z = lis.magnetic
    #print(f"X:{mag_x:.2f}, Y:{mag_y:.2f}, Z:{mag_z:.2f} uT")
    #print()    

    # Angenommen, dies sind Ihre X-, Y- und Z-Werte
    x = mag_x
    y = mag_y
    z = mag_z

    # Berechnen Sie den Winkel in Radian
    winkel_rad = math.atan2(y, x)

    # Konvertieren Sie den Winkel in Grad
    winkel_grad = math.degrees(winkel_rad)

    # Normalisieren Sie den Winkel auf den Bereich 0 bis 360
    if winkel_grad < 0:
        winkel_grad += 360
        
    print(winkel_grad)
    sleep_ms(500)


