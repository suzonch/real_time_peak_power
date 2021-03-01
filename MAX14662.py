# 8 channel SPST switch
from smbus2 import SMBus


bus = SMBus(1)

slave_address = 0x4c
reg_address = 0x0     # device has only one register

off = 0x0
sw1 = 0x1
sw2 = 0x3
sw3 = 0x7
sw4 = 0xF
sw5 = 0x1F
sw6 = 0x3F
sw7 = 0x7F
sw8 = 0xFF


class MAX14662:
    _readFn = None
    _writeFn = None

    def __init__(self, readFn, writeFn):
        self._readFn = readFn
        self._writeFn = writeFn

    def _read_reg(self):
        val = self._readFn(slave_address, reg_address, 1)
        return val

    def switch_off(self):
        self._writeFn(slave_address, reg_address, [off])

    def switch1(self):
        self._writeFn(slave_address, reg_address, [sw1])

    def switch2(self):
        self._writeFn(slave_address, reg_address, [sw2])

    def switch3(self):
        self._writeFn(slave_address, reg_address, [sw3])

    def switch4(self):
        self._writeFn(slave_address, reg_address, [sw4])

    def switch5(self):
        self._writeFn(slave_address, reg_address, [sw5])

    def switch6(self):
        self._writeFn(slave_address, reg_address, [sw6])

    def switch7(self):
        self._writeFn(slave_address, reg_address, [sw7])

    def switch8(self):
        self._writeFn(slave_address, reg_address, [sw8])


turn = MAX14662(bus.read_i2c_block_data, bus.write_i2c_block_data)

turn.switch1()
turn.switch_off()


