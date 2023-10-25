from machine import I2C, Pin
i2c = I2C(1, freq=100000, scl=Pin(1), sda=Pin(0))

# enable channel 0,1,2,3 (SD0,SC0)
i2c.writeto(0x70, b'\xF')
i2c.scan()

# enable channel 0 (SD0,SC0)
i2c.writeto(0x70, b'\x01')
i2c.scan()

# enable channel 1 (SD1,SC1)
i2c.writeto(0x70, b'\x01')
i2c.scan()

# enable channel 2 (SD2,SC2)
i2c.writeto(0x70, b'\x01')
i2c.scan()

# enable channel 3 (SD3,SC3)
i2c.writeto(0x70, b'\x01')
i2c.scan()


# read which channels are enabled?
i2c.readfrom(0x70, 1)
