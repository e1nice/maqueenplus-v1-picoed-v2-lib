from picoed_v2_lib import *
from .maqueenplus import *

i2c0 = I2C(IIC.BUS0, scl=Pin(IIC.SCL0), sda=Pin(IIC.SDA0))
i2c1 = I2C(IIC.BUS1, scl=Pin(IIC.SCL1), sda=Pin(IIC.SDA1), freq=100000)
display = Display(i2c0)
pe_led = Led()
button_a = Button(Gpio.BUTTON_A)
button_b = Button(Gpio.BUTTON_B)
music = Music(Pin(Gpio.BUZZER))
mq = MaqueenPlus(i2c1)
