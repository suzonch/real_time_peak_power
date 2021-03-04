from smbus2 import SMBus
from transition_stage import *
from LTC2606 import *
from capture_spectra import *
from PAC193X import *
from temp_control import *

bus = SMBus(1)



ltc_tec1 = 0x11
ltc_addr_led = 0x10

set_temp(ltc_tec1, 23)
test.set_current(ltc_addr_led, 200, 0.127)
time.sleep(120)



transition = MOX06XXX(1)
transition.start_test()


