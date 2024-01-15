from machine import mem32, Pin
#auf 0x00 befinden sich das Vol tage Select-Register: 0b0=3,3V , 0b1=1,8V
#0x04=gp0, 0x08=gp1, usw.

PADS_BANK0_BASE = 0x4001c000
#Datenblatt

gpX = 11 #11=Bremse 12=PSU 24V 13=Lüfter
maxStrom = 0x3 #0x3 → 12mA

#ab 0x04 von Grundadresse in 4er Schritten springen. 
adr = PADS_BANK0_BASE + 0x04 + gpX * 4 
#Bit 5:4 auf 0 setzen und mit XOR 5:4 auf 11
mem32[adr] = mem32[adr] & 11001111 ^ (maxStrom<<4)

#led=Pin(gpX, Pin.OUT, value=0)
#led.value(1)
