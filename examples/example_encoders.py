from maqueenplus_v1_picoed_v2_lib import *
from time import sleep_ms
from picoed_v2_lib import *
from machine import Pin, I2C


i2c1 = I2C(IIC.BUS1, scl=Pin(IIC.SCL1), sda=Pin(IIC.SDA1), freq=100000)
mq = MaqueenPlus(i2c1)
button_a = Button(Gpio.BUTTON_A)
button_b = Button(Gpio.BUTTON_B)

button_a.was_pressed()
button_b.was_pressed()

mq.clear_encoders()
print("encoders: {}".format(mq.encoders))

while not (button_a.is_pressed() and button_b.is_pressed()):
    if button_a.was_pressed():
        mq.clear_encoder_right()
    if button_b.was_pressed():
        mq.clear_encoder_left()
    enc_l = mq.encoder_left
    print("left: {}".format(enc_l))
    enc_r = mq.encoder_right
    print("right: {}".format(enc_r))
    print("encoders: {}".format(mq.encoders))
    sleep_ms(1000)
mq.clear_encoders()
print("encoders: {}".format(mq.encoders))
