import machine
import struct


class I2cDev:
    def __init__(self, i2c: machine.I2C, address):
        self._i2c = i2c
        self._address = address

    def write(self, register, fmt: str, *values):
        buf = struct.pack("B", register) + struct.pack(fmt, *values)
        self._i2c.writeto(self._address, buf)

    def read(self, register, parm):
        if type(parm) == int:
            self._i2c.writeto(self._address, struct.pack("B", register))
            return self._i2c.readfrom(self._address, parm)
        length = struct.calcsize(parm)
        self._i2c.writeto(self._address, struct.pack("B", register))
        return struct.unpack(parm, self._i2c.readfrom(self._address, length))

    def read_string(self, register, length):
        return self.read(register, length).decode()
