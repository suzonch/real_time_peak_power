from smbus2 import SMBus

bus = SMBus(1)

switch = 0x4c

bus.write_i2c_block_data(switch, 0b00, [0b00000001])