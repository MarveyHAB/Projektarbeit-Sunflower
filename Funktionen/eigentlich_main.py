import veml7700
from hmc5883l import HMC5883L
from sonne_jan import getAZ, getSEA
from stepperansteuerung_2 import step #sunPos

from time import sleep, sleep_ms

AZ = getAZ(51,7,2)
SE = getSEA(51,7,2)
print("Sonnenrichtung:", AZ)
print("Sonnenhöhe:" ,SE)
step(int(AZ))