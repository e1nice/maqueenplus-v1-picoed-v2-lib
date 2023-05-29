from maqueenplus_v1_picoed_v2_lib import *
from time import sleep_ms
from picoed_v2_lib import *
from machine import Pin, I2C


i2c1 = I2C(IIC.BUS1, scl=Pin(IIC.SCL1), sda=Pin(IIC.SDA1), freq=100000)
mq = MaqueenPlus(i2c1)
mq.line_bw_threshold = 2600

for x in range(10):
    print("Line sensors black - auto (L3, L2, L1, R1, R2, R3)    : {}.".format(mq.line_bw_auto))
    print("Line sensors black - threshold (L3, L2, L1, R1, R2, R3)    : {}.".format(mq.line_bw))
    print("Line sensors black split - threshold (L3, L2, L1, R1, R2, R3): {}.".format(mq.line_bw_split))
    print("Line sensors grayscale all (L3, L2, L1, R1, R2, R3): {}.".format(mq.line_grays))
    print("Line sensors grayscale each (L3, L2, L1, R1, R2, R3): {}, {}, {}, {}, {}, {}."
          .format(mq.line_gray_l3, mq.line_gray_l2, mq.line_gray_l1, mq.line_gray_r1, mq.line_gray_r2, mq.line_gray_r3))
    print()
    sleep_ms(2000)
    