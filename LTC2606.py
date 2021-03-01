#16 bit DAC
import math
from smbus2 import SMBus
import time

class DAC:
    vref = 0
    bitcount = 0
    vref = 0
    _writeFn = None

    def __init__(self, ref_voltage, nm_bits, wr):
        self.vref = ref_voltage
        self.bitcount = nm_bits
        self._writeFn = wr

class LTC2606(DAC):
    bitcount = 16
                        #set in milivolt

    def __init__(self, ref_voltage, wr):
        super(LTC2606, self).__init__(ref_voltage, self.bitcount, wr)

    def set_voltage(self, addr, mili_volt):
        lsb_value = self.vref / pow(2, self.bitcount)
        val = math.floor(mili_volt/lsb_value)
        vout = val * lsb_value
        print('Setting LTC2606 voltage to {}mV (bits: {})'.format(vout, bin(val)))
        reg = 0b00110000
        byte1 = (val >> 8)
        byte2 = val & 0xFF
        print(bin(byte1))
        print(bin(byte2))
        self._writeFn(addr, reg, [byte1, byte2])
        return val


    def set_current(self, addr, current, send_res):
        target_voltage = current * send_res
        self.set_voltage(addr, target_voltage)
        print('Setting current to:~', current)



bus = SMBus(1)

# ltc_addr_led = 0x10     #LED DAC
# test = LTC2606(3300, bus.write_i2c_block_data)
# test.set_current(ltc_addr_led, 100, 0.127)




