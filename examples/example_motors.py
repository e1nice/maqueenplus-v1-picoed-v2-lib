from maqueenplus_v1_picoed_v2_lib import *
from time import sleep_ms
from picoed_v2_lib import *
from machine import Pin, I2C

i2c1 = I2C(IIC.BUS1, scl=Pin(IIC.SCL1), sda=Pin(IIC.SDA1), freq=100000)
mq = MaqueenPlus(i2c1)

mq.motors = (0, 0)
mq.clear_encoders()
mq.pid = True
print("motors: {}".format(mq.motors))
mq.motors = (250, -120)
print("motors: {}".format(mq.motors))
for x in range(10):
    sleep_ms(1000)
    print("motors: {}".format(mq.motors))
    print("encoders: {}".format(mq.encoders))
print("STOP")
mq.motors = (0, 0)
for x in range(3):
    sleep_ms(1000)
    print("motors: {}".format(mq.motors))
    print("encoders: {}".format(mq.encoders))
print("THE END")
