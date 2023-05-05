from maqueenplus_v1_picoed_v2_lib import *
from time import sleep_ms
from picoed_v2_lib import *
from machine import Pin, I2C


i2c1 = I2C(IIC.BUS1, scl=Pin(IIC.SCL1), sda=Pin(IIC.SDA1), freq=100000)
mq = MaqueenPlus(i2c1)

for x in range(10):
    print("Line sensors black (L3, L2, L1, R1, R2, R3)    : {}.".format(mq.line_bw))
    print("Line sensors grayscale (L3, L2, L1, R1, R2, R3): {}.".format(mq.line_gray))
    print()
    sleep_ms(2000)
    