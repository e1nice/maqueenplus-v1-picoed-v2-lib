from maqueenplus_v1_picoed_v2_lib import *
from time import sleep_ms
from picoed_v2_lib import *
from machine import Pin, I2C

i2c1 = I2C(IIC.BUS1, scl=Pin(IIC.SCL1), sda=Pin(IIC.SDA1), freq=100000)
mq = MaqueenPlus(i2c1)

mq.pid = mq.PID.ON
print("pid: {}".format(mq.pid))
mq.pid = mq.PID.OFF
print("pid: {}".format(mq.pid))
