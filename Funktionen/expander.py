from machine import I2C, Pin
import VEML7700
i2c = I2C(1, freq=100000, scl=Pin(1), sda=Pin(0))

# enable channel 0,1,2,3 (SD0,SC0)
#i2c.writeto(0x70, b'\xF')
#i2c.scan()

# enable channel 0 (SD0,SC0)
i2c.writeto(0x70, b'\x01')
i2c.scan()
LichtOben = i2c.VEML7700.read_lux()

# enable channel 1 (SD1,SC1)
i2c.writeto(0x70, b'\x02')
i2c.scan()
LichtUben = i2c.VEML7700.read_lux()

# enable channel 2 (SD2,SC2)
i2c.writeto(0x70, b'\x04')
i2c.scan()
LichtLinks = i2c.VEML7700.read_lux()

# enable channel 3 (SD3,SC3)
i2c.writeto(0x70, b'\x08')
i2c.scan()
LichtOrechts = i2c.VEML7700.read_lux()

# read which channels are enabled?
i2c.readfrom(0x70, 1)
