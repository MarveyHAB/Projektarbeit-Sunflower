from sh1106		import SH1106_I2C
from machine 	import Pin, RTC, I2C, Timer
from time		import sleep, sleep_ms

#Display
i2c 	= I2C(0, scl=Pin(1), sda=Pin(0))
display = SH1106_I2C(128, 64, i2c, Pin(28), 0x3c)

display.fill(0)
display.text('Sunflower', 0,  0, 1)
display.text('Jan'   , 0, 10, 1)
display.show()

'''

display.text('Zeile 1 Start', 0, 0, 1)
display.text('Zeile 2 Start', 0, 10, 1)
display.text('Zeile 3 Start', 0, 20, 1)
display.text('Zeile 4 Start', 0, 30, 1)
display.text('Zeile 5 Start', 0, 40, 1)
display.text('Zeile 6 Start', 0, 50, 1)
display.show()
sleep(3)

display.fill(0)
display.text('Mitte',40, 0, 1)
display.show()
sleep(1)
'''