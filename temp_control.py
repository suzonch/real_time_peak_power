# NTC model: NTCALUG03A103G
import math
from LTC2606 import *
from ADC121C021 import *

bus = SMBus(1)

def temp_from_R(r):
    t = 1/((1/298.15) + ((1/3984) * math.log(r/9965)))
    t_celsius = t - 273.15
    return t_celsius

def get_temp(addr):
    adc = ADC121C021(bus.write_i2c_block_data, bus.read_i2c_block_data)
    vout = adc.read_adc(addr) * 1000
    resistance = (vout * 9960) / (1500 - vout)
    temp_in_c = temp_from_R(resistance)
    return temp_in_c


def set_temp(addr, c):
     # Peltier DAC
    test = LTC2606(1500, bus.write_i2c_block_data)
    if c<= 25:
        adc_val = 750 + (25 - c) * 17.2
        test.set_voltage(addr, adc_val)
    elif c>25:
        adc_val2 = 750 - (c - 25) * 17
        test.set_voltage(addr, adc_val2)


# ltc_addr_tec = 0x11
# #set_temp(ltc_addr_tec, 25)
#
# adc_addr = 0x50
# print("TEC temp:", get_temp(adc_addr))
