#12 bit ADC
from smbus2 import  SMBus


class ADC121C021:
    _writeFn = None
    _readFn = None

    def __init__(self, wr, rd):
        self._writeFn = wr
        self._readFn = rd

    def read_adc(self, address):                # return adc value in volt(not milivolt)
        meas = self._readFn(address, 0b0, 2)
        meast = ((meas[0]) << 8) | (meas[1])
        val = meast & 0b0000111111111111
        adc_val = val
        final_value = adc_val / pow(2, 12) * 3.3
        return final_value

