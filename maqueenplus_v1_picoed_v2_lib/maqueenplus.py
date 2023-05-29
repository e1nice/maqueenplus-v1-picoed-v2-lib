from machine import I2C
from .i2c_dev import I2cDev
from .enum_dict import EnumDict


class _Ic2Reg:
    MOTOR_LEFT_DIR = 0x00
    MOTOR_LEFT_SPD = 0x01
    MOTOR_RIGHT_DIR = 0x02
    MOTOR_RIGHT_SPD = 0x03
    ENCODER_LEFT = 0x04
    ENCODER_RIGHT = 0x06
    PID = 0x0a
    LED_LEFT = 0x0b
    LED_RIGHT = 0x0c
    SERVO_S1 = 0x14
    SERVO_S2 = 0x15
    SERVO_S3 = 0x16
    LINE_BW = 0x1d
    LINE_GRAY_L3 = 0x1e
    LINE_GRAY_L2 = 0x20
    LINE_GRAY_L1 = 0x22
    LINE_GRAY_R1 = 0x24
    LINE_GRAY_R2 = 0x26
    LINE_GRAY_R3 = 0x28
    VERSION_LEN = 0x32
    VERSION_DATA = 0x33


class _Rgb(EnumDict):
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    PINK = 5
    CYAN = 6
    WHITE = 7
    OFF = 0


class _Gray:
    L3 = _Ic2Reg.LINE_GRAY_L3
    L2 = _Ic2Reg.LINE_GRAY_L2
    L1 = _Ic2Reg.LINE_GRAY_L1
    R1 = _Ic2Reg.LINE_GRAY_R1
    R2 = _Ic2Reg.LINE_GRAY_R2
    R3 = _Ic2Reg.LINE_GRAY_R3


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
    GRAY = _Gray()
    _DEFAULT_LINE_THRESHOLD = 2500

    def __init__(self, i2c: I2C, address=0x10):
        self._mq_i2c = I2cDev(i2c, address)
        self._address = address
        self._ENCODER_TICKS = 80
        self._line_threshold = self._DEFAULT_LINE_THRESHOLD

    @property
    def motors(self):
        left_direction, left_speed, right_direction, right_speed = self._mq_i2c.read(self.I2C_REG.MOTOR_LEFT_DIR, "BBBB")
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
        self._mq_i2c.write(self.I2C_REG.MOTOR_LEFT_DIR, "BBBB", left_direction, left_speed, right_direction, right_speed)

    @property
    def motor_left(self):
        direction, speed = self._mq_i2c.read(self.I2C_REG.MOTOR_LEFT_DIR, "BB")
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
        self._mq_i2c.write(self.I2C_REG.MOTOR_LEFT_DIR, "BB", direction, speed)

    @property
    def motor_right(self):
        direction, speed = self._mq_i2c.read(self.I2C_REG.MOTOR_RIGHT_DIR, "BB")
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
        self._mq_i2c.write(self.I2C_REG.MOTOR_RIGHT_DIR, "BB", direction, speed)

    @property
    def encoders(self):
        return self._mq_i2c.read(self.I2C_REG.ENCODER_LEFT, ">HH")

    def clear_encoders(self):
        self._mq_i2c.write(self.I2C_REG.ENCODER_LEFT, ">HH", 0, 0)

    @property
    def encoder_left(self):
        return self._mq_i2c.read(self.I2C_REG.ENCODER_LEFT, ">H")[0]

    def clear_encoder_left(self):
        self._mq_i2c.write(self.I2C_REG.ENCODER_LEFT, ">H", 0)

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
    def rgbs(self):
        return self._mq_i2c.read(self.I2C_REG.LED_LEFT, "BB")

    @rgbs.setter
    def rgbs(self, left_right: (int, int)):
        try:
            left, right = left_right
        except ValueError:
            raise ValueError("Pass an iterable with two values, for left and right rgb led.")
        else:
            self._mq_i2c.write(self.I2C_REG.LED_LEFT, "BB", left % 8, right % 8)

    @property
    def rgb_left(self):
        return self._mq_i2c.read(self.I2C_REG.LED_LEFT, "B")[0]

    @rgb_left.setter
    def rgb_left(self, value: int):
        self._mq_i2c.write(self.I2C_REG.LED_LEFT, "B", value % 8)

    @property
    def rgb_right(self):
        return self._mq_i2c.read(self.I2C_REG.LED_RIGHT, "B")[0]

    @rgb_right.setter
    def rgb_right(self, value: int):
        self._mq_i2c.write(self.I2C_REG.LED_RIGHT, "B", value % 8)

    @property
    def servos(self):
        return self._mq_i2c.read(self.I2C_REG.SERVO_S1, "BBB")[0]

    @servos.setter
    def servos(self, s1_s2_s3: (int, int, int)):
        try:
            s1, s2, s3 = s1_s2_s3
        except ValueError:
            raise ValueError("Pass an iterable with three values, for sensor 1, 2 and 3.")
        degrees1 = max(0, min(180, s1))
        degrees2 = max(0, min(180, s2))
        degrees3 = max(0, min(180, s3))
        self._mq_i2c.write(self.I2C_REG.SERVO_S1, "BBB", degrees1, degrees2, degrees3)

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
    def line_bw_threshold(self):
        return self._line_threshold

    @line_bw_threshold.setter
    def line_bw_threshold(self, line_threshold):
        self._line_threshold = line_threshold

    @property
    def line_bw_auto(self):
        return self._mq_i2c.read(self.I2C_REG.LINE_BW, "B")[0]

    @property
    def line_bw_auto_split(self):
        bw = self._mq_i2c.read(self.I2C_REG.LINE_BW, "B")[0]
        s = []
        for i in range(6):
            s.append(bw & 2 ** i > 0)
        return tuple(s)

    @property
    def line_bw(self):
        grays = self._mq_i2c.read(self.I2C_REG.LINE_GRAY_L3, ">HHHHHH")
        s = 0
        for i in range(6):
            if grays[i] < self._line_threshold:
                s += 2 ** i
        return s

    @property
    def line_bw_split(self):
        grays = self._mq_i2c.read(self.I2C_REG.LINE_GRAY_L3, ">HHHHHH")
        s = []
        for i in range(6):
            s.append(grays[i] < self._line_threshold)
        return tuple(s)

    @property
    def line_grays(self):
        return self._mq_i2c.read(self.I2C_REG.LINE_GRAY_L3, ">HHHHHH")

    def line_gray(self, sensor):
        return self._mq_i2c.read(sensor, ">H")[0]

    @property
    def line_gray_l3(self):
        return self._mq_i2c.read(self.I2C_REG.LINE_GRAY_L3, ">H")[0]

    @property
    def line_gray_l2(self):
        return self._mq_i2c.read(self.I2C_REG.LINE_GRAY_L2, ">H")[0]

    @property
    def line_gray_l1(self):
        return self._mq_i2c.read(self.I2C_REG.LINE_GRAY_L1, ">H")[0]

    @property
    def line_gray_r1(self):
        return self._mq_i2c.read(self.I2C_REG.LINE_GRAY_R1, ">H")[0]

    @property
    def line_gray_r2(self):
        return self._mq_i2c.read(self.I2C_REG.LINE_GRAY_R2, ">H")[0]

    @property
    def line_gray_r3(self):
        return self._mq_i2c.read(self.I2C_REG.LINE_GRAY_R3, ">H")[0]

    @property
    def version(self):
        v_len = self._mq_i2c.read(self.I2C_REG.VERSION_LEN, "B")[0]
        return self._mq_i2c.read_string(self.I2C_REG.VERSION_DATA, v_len)
