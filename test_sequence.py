from smbus2 import SMBus
from transition_stage import *
from LTC2606 import *
from capture_spectra import *
from PAC193X import *
from temp_control import *

bus = SMBus(1)



def tec_temp():  # will update this to work with temp set point rather than voltage setpoint
    ltc_tec1 = 0x11
    



def led_current():
    ltc_led1 = 0x10
    led_obj = LTC2606(3300, bus.write_i2c_block_data)
    led_obj.set_current(ltc_led1, 200, 0.127)