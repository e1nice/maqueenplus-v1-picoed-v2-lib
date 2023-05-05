from machine import I2C
from .i2c_dev import I2cDev
from .enum_dict import EnumDict


class _Ic2Reg:
    MOTORS = 0x00
    MOTOR_LEFT = 0x01
    MOTOR_RIGHT = 0x02
    ENCODERS = 0x04
    ENCODER_RIGHT = 0x06
    PID = 0x0a
    LEDS = 0x0b
    LED_RIGHT = 0x0c
    SERVO_S1 = 0x14
    SERVO_S2 = 0x15
    SERVO_S3 = 0x16
    LINE_BW = 0x1d
    LINE_GRAY = 0x1e
    VERSION_LEN = 0x32
    VERSION_DATA = 0x33


class _Rgb(EnumDict):
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    PINK = 5
    CYAN = 6
    WHITE = 7
    OFF = 0


class _MotorDirection:
    HOLD = 0
    FORWARD = 1
    BACKWARD = 2


class _Pid:
    ON = True
    OFF = False


class MaqueenPlus:
    I2C_REG = _Ic2Reg()
    RGB = _Rgb()
    MOTOR_DIR = _MotorDirection()
    PID = _Pid()

    def __init__(self, i2c: I2C, address=0x10):
        self._mq_i2c = I2cDev(i2c, address)
        self._address = address
        self._ENCODER_TICKS = 80

    @property
    def motor_left(self):
        direction, speed = self._mq_i2c.read(self.I2C_REG.MOTORS, "BB")
        if direction == self.MOTOR_DIR.BACKWARD:
            value = -1 * speed
        else:
            value = direction * speed
        return value

    @motor_left.setter
    def motor_left(self, value: int):
        if value < 0:
            direction = self.MOTOR_DIR.BACKWARD
            speed = min(240, -1 * value)
        else:
            direction = self.MOTOR_DIR.FORWARD
            speed = min(240, value)
        self._mq_i2c.write(self.I2C_REG.MOTORS, "BB", direction, speed)

    @property
    def motors(self):
        left_direction, left_speed, right_direction, right_speed = self._mq_i2c.read(self.I2C_REG.MOTORS, "BBBB")
        if left_direction == self.MOTOR_DIR.BACKWARD:
            left = -1 * left_speed
        else:
            left = left_direction * left_speed
        if right_direction == self.MOTOR_DIR.BACKWARD:
            right = -1 * right_speed
        else:
            right = right_direction * right_speed
        return left, right

    @motors.setter
    def motors(self, left_right: (int, int)):
        try:
            left, right = left_right
        except ValueError:
            raise ValueError("Pass an iterable with two values, for left and right motor.")
        else:
            if left < 0:
                left_direction = self.MOTOR_DIR.BACKWARD
                left_speed = min(240, -1 * left)
            else:
                left_direction = self.MOTOR_DIR.FORWARD
                left_speed = min(240, left)
            if right < 0:
                right_direction = self.MOTOR_DIR.BACKWARD
                right_speed = min(240, -1 * right)
            else:
                right_direction = self.MOTOR_DIR.FORWARD
                right_speed = min(240, right)
        self._mq_i2c.write(self.I2C_REG.MOTORS, "BBBB", left_direction, left_speed, right_direction, right_speed)

    @property
    def motor_right(self):
        direction, speed = self._mq_i2c.read(self.I2C_REG.MOTOR_RIGHT, "BB")
        if direction == self.MOTOR_DIR.BACKWARD:
            value = -1 * speed
        else:
            value = direction * speed
        return value

    @motor_right.setter
    def motor_right(self, value: int):
        if value < 0:
            direction = self.MOTOR_DIR.BACKWARD
            speed = min(240, -1 * value)
        else:
            direction = self.MOTOR_DIR.FORWARD
            speed = min(240, value)
        self._mq_i2c.write(self.I2C_REG.MOTOR_RIGHT, "BB", direction, speed)

    @property
    def encoder_left(self):
        return self._mq_i2c.read(self.I2C_REG.ENCODERS, ">H")[0]

    def clear_encoder_left(self):
        self._mq_i2c.write(self.I2C_REG.ENCODERS, ">H", 0)

    @property
    def encoders(self):
        return self._mq_i2c.read(self.I2C_REG.ENCODERS, ">HH")

    def clear_encoders(self):
        self._mq_i2c.write(self.I2C_REG.ENCODERS, ">HH", 0, 0)

    @property
    def encoder_right(self):
        return self._mq_i2c.read(self.I2C_REG.ENCODER_RIGHT, ">H")[0]

    def clear_encoder_right(self):
        self._mq_i2c.write(self.I2C_REG.ENCODER_RIGHT, ">H", 0)

    @property
    def pid(self):
        return self._mq_i2c.read(self.I2C_REG.PID, "B")[0] > 0

    @pid.setter
    def pid(self, on: bool):
        self._mq_i2c.write(self.I2C_REG.PID, "B", on)

    @property
    def rgb_left(self):
        return self._mq_i2c.read(self.I2C_REG.LEDS, "B")[0]

    @rgb_left.setter
    def rgb_left(self, value: int):
        self._mq_i2c.write(self.I2C_REG.LEDS, "B", value % 8)

    @property
    def rgbs(self):
        return self._mq_i2c.read(self.I2C_REG.LEDS, "BB")

    @rgbs.setter
    def rgbs(self, left_right: (int, int)):
        try:
            left, right = left_right
        except ValueError:
            raise ValueError("Pass an iterable with two values, for left and right rgb led.")
        else:
            self._mq_i2c.write(self.I2C_REG.LEDS, "BB", left % 8, right % 8)

    @property
    def rgb_right(self):
        return self._mq_i2c.read(self.I2C_REG.LED_RIGHT, "B")[0]

    @rgb_right.setter
    def rgb_right(self, value: int):
        self._mq_i2c.write(self.I2C_REG.LED_RIGHT, "B", value % 8)

    @property
    def s1(self):
        return self._mq_i2c.read(self.I2C_REG.SERVO_S1, "B")[0]

    @s1.setter
    def s1(self, degrees: int):
        value = max(0, min(180, degrees))
        self._mq_i2c.write(self.I2C_REG.SERVO_S1, "B", value)

    @property
    def s2(self):
        return self._mq_i2c.read(self.I2C_REG.SERVO_S2, "B")[0]

    @s2.setter
    def s2(self, degrees: int):
        value = max(0, min(180, degrees))
        self._mq_i2c.write(self.I2C_REG.SERVO_S2, "B", value)

    @property
    def s3(self):
        return self._mq_i2c.read(self.I2C_REG.SERVO_S3, "B")[0]

    @s3.setter
    def s3(self, degrees: int):
        value = max(0, min(180, degrees))
        self._mq_i2c.write(self.I2C_REG.SERVO_S3, "B", value)

    @property
    def line_bw(self):
        bw = self._mq_i2c.read(self.I2C_REG.LINE_BW, "B")[0]
        s = []
        for i in range(6):
            s.append(bw & 2 ** i > 0)
        return tuple(s)

    @property
    def line_gray(self):
        return self._mq_i2c.read(self.I2C_REG.LINE_GRAY, ">HHHHHH")

    @property
    def version(self):
        v_len = self._mq_i2c.read(self.I2C_REG.VERSION_LEN, "B")[0]
        return self._mq_i2c.read_string(self.I2C_REG.VERSION_DATA, v_len)

    # def get_us_mm(self):
    #     if ticks_diff(ticks_ms(), self._us_last_ticks_ms) < self._US_INTERVAL_MS:
    #         return self._us_last_mm
    #     self._us_last_ticks_ms = ticks_ms()
    #
    #     self._US_TRIG_PIN.value(0)
    #     self._US_TRIG_PIN.value()
    #     self._US_TRIG_PIN.value(1)
    #     self._US_TRIG_PIN.value(0)
    #     us = time_pulse_us(self._US_ECHO_PIN, 1, 10500)
    #
    #     if us > 0:
    #         mm = us * 0.1715
    #     else:
    #         mm = 9999
    #     return mm
