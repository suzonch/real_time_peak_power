from smbus2 import SMBus
from csv import writer
from PAC193X import *
from temp_control import *


bus = SMBus(1)


def saveiv_t(pac_address, adc_address, folder):
    temprature = get_temp(adc_address, 1500)
    currentpre = (getiv(pac_address))
    current_t = [int(time.time()), "{:.4f}".format(currentpre[0]), "{:.4f}".format(currentpre[1]), "{:.4f}".format(temprature) ]
#    current_t = '{},\t{:.4f},\t{:.4f},\t{:.4f}'.format(int(time.time()), currentpre[0], currentpre[1], temprature)


    with open('/home/pi/PycharmProjects/LED_Test_all/output/'+folder+'/iv_t.csv', 'a') as f:
        write = writer(f)
        write.writerow(current_t)


adc_addr = 0x50
pac_addr = 0x1E

#saveiv_t(pac_addr, adc_addr, "LED1")