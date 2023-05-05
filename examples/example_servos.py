from maqueenplus_v1_picoed_v2_lib import *
from time import sleep_ms
from picoed_v2_lib import *
from machine import Pin, I2C

i2c1 = I2C(IIC.BUS1, scl=Pin(IIC.SCL1), sda=Pin(IIC.SDA1), freq=100000)
mq = MaqueenPlus(i2c1)

print("--- test servo 1 ---")
for angle in range(-5, 191, 15):
    print("Set angle to {} degrees.".format(angle))
    mq.s1 = angle
    sleep_ms(500)
    print("Resulting angle: {}.".format(mq.s1))
mq.s1 = 90
sleep_ms(500)

print("--- test servo 2 ---")
for angle in range(-5, 191, 15):
    print("Set angle to {} degrees.".format(angle))
    mq.s2 = angle
    sleep_ms(500)
    print("Resulting angle: {}.".format(mq.s2))
mq.s2 = 90
sleep_ms(500)

print("--- test servo 3 ---")
for angle in range(-5, 191, 15):
    print("Set angle to {} degrees.".format(angle))
    mq.s3 = angle
    sleep_ms(500)
    print("Resulting angle: {}.".format(mq.s3))
mq.s3 = 90
sleep_ms(500)
