from maqueenplus_v1_picoed_v2_lib import *
from time import sleep_ms
from picoed_v2_lib import *
from machine import Pin, I2C

i2c1 = I2C(IIC.BUS1, scl=Pin(IIC.SCL1), sda=Pin(IIC.SDA1), freq=100000)
mq = MaqueenPlus(i2c1)

print("--- both leds ---")
for color in mq.RGB:
    print("Color: {}".format(color[0]))
    mq.rgbs = (color[1], color[1])
    print(mq.rgbs)
    sleep_ms(1000)
mq.rgbs = (mq.RGB.OFF, mq.RGB.OFF)

print("--- left led ---")
for color in mq.RGB:
    print("Color: {}".format(color[0]))
    mq.rgb_left = color[1]
    print(mq.rgb_left)
    sleep_ms(1000)
mq.rgb_left = mq.RGB.OFF

print("--- right led ---")
for color in mq.RGB:
    print("Color: {}".format(color[0]))
    mq.rgb_right = color[1]
    print(mq.rgb_right)
    sleep_ms(1000)
mq.rgb_right = mq.RGB.OFF
