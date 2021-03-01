import time
from enum import Enum
import logging
from smbus2 import SMBus

# address mappings
CMD_REFRESH = 0x00
REG_CTRL = 0x01
REG_ACC_COUNT = 0x02
REG_VPOW_ACC_BASE = 0x03
REG_VBUS_BASE = 0x07
REG_VSENSE_BASE = 0x0B
REG_VBUS_AVG_BASE = 0x0F
REG_VSENSE_AVG_BASE = 0x13
REG_VPOWER_BASE = 0x17
REG_CHANNEL_DIS = 0x1C
REG_NEG_PWR = 0x1D
CMD_REFRESH_G = 0x1E
CMD_REFRESH_V = 0x1F
REG_SLOW = 0x20
REG_CTRL_ACT = 0x21
REG_CHANNEL_DIS_ACT = 0x22
REG_NEG_PWR_ACT = 0x23
REG_CTRL_LAT = 0x24
REG_DISL_LAT = 0x25
REG_NEW_PWR_LAT = 0x26
REG_PRODUCT_ID = 0xFD  # should be 0x5B
REG_MFR_ID = 0xFE  # should be 0x5D
REG_REV_ID = 0xFF  # should be 0x03


class SampleRate(Enum):
    rate1024 = 0b00
    rate256 = 0b01
    rate64 = 0b10
    rate8 = 0b11


class Channel(Enum):
    A = 0x00
    B = 0x01
    C = 0x02
    D = 0x03


class PAC1934:
    shunt1 = 1.0
    shunt2 = 1.0
    shunt3 = 1.0
    shunt4 = 1.0
    readFn = None
    log = None
    '''
    readFn(addr, n) should read n bytes from the device register addr
    and return bytes
    '''

    def __init__(self, readFn, writebytFn, writeblockFn):
        self.readFn = readFn
        self.writebytFn = writebytFn
        self.writeblockFn = writeblockFn
        self.log = logging.getLogger('PAC')

    def checkDev(self):
        data = self.readReg(REG_PRODUCT_ID, 3)
        if (data[0] == 0x5B) and (data[1] == 0x5D) and (data[2] == 0x03):
            return True
        self.log.error('Could not find PAC192x with given address!')
        return False

    def setShuntRValues(self, v1, v2, v3, v4):
        self.shunt1 = v1
        self.shunt2 = v2
        self.shunt3 = v3
        self.shunt4 = v4

    # returns bus voltage in V
    def getVbus(self, channel: Channel):
        data = self.readReg(REG_VBUS_BASE + channel.value, 2)
        print(channel.value)
        adcVal = mergeBytes(data)
        lsb =  (32 / pow(2, 16))
        print(adcVal, data)
#        print("Data in bin",bin(data[0]), bin(data[1]))
        voltage = adcVal * lsb
        return voltage

    # returns sensed current in mA
    def getCurrent(self, channel: Channel):
        data = self.readReg(REG_VSENSE_BASE + channel.value, 2)
        adcVal = mergeBytes(data)
        print(bin(adcVal))
        FSC = 100 / 0.1
        current = FSC * adcVal / pow(2, 16)
        return current

    # refresh readout registers without resetting accumulators
    def refreshV(self):
        self.writeReg(CMD_REFRESH_V, [])

    def readReg(self, reg, numBytes):
        self.log.debug('>: [%s], expect: %d', hex(reg), numBytes)
        val = self.readFn(pac_addr, reg, numBytes)
        self.log.debug('<: [{}]'.format(','.join(hex(x) for x in val)))
        return val

    def writeReg(self, address, reg):
        self.writebytFn(address, reg)

    def writeRegData(self,address, reg, data):
        self.log.debug('>: [%s], data', hex(reg), data)
        self.writeblockFn(address, reg, [data])


def mergeBytes(arr):
    return (arr[0] << 8) | arr[1]

pac_addr = 0x1E

bus = SMBus(1)

def getiv(addr):
    pacobj = PAC1934(bus.read_i2c_block_data, bus.write_byte, bus.write_i2c_block_data)

    pacobj.writeReg(addr, CMD_REFRESH)
    time.sleep(.001)
    pacobj.writeRegData(addr, REG_CTRL, 0b01010000)
    time.sleep(.001)
    pacobj.writeRegData(addr, REG_CHANNEL_DIS, 0b00000010)

    current = pacobj.getCurrent(Channel.B)
    high = pacobj.getVbus(channel= Channel.C)
    time.sleep(.001)
    low = pacobj.getVbus(channel= Channel.A)
    voltage_drop = high - low
    return [current, voltage_drop]


#print(getiv(pac_addr))



