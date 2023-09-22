'''from time import sleep_ms
from machine import Pin, SoftI2C

i2c  =  SoftI2C( scl=Pin(1) , sda=Pin(0))
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))
 
  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))
'''
import veml7700
from hmc5883l import HMC5883L
from Sonne import getAZ, getSEA

from time import sleep, sleep_ms
from machine import Pin, SoftI2C

#i2c  =  SoftI2C( scl=Pin(1) , sda=Pin(0))
#veml = veml7700.VEML7700(address=0x10, i2c=i2c, it=100, gain=1/8)

while True:
    AZ = getAZ(51,7,2)
    SE = getSEA(51,7,2)
    print("Sonnenrichtung:", AZ)
    print("Sonnenhöhe:" ,SE)
    sleep(10)
    '''
    veml = veml7700.VEML7700(address=0x10, i2c=i2c, it=100, gain=1/8)
    lux_val = veml.read_lux()
    print("Helligkeit in lux: ",lux_val)
    sleep_ms(500)
    '''