# this code includes most of sequencing of other devices in test
# switch at the back of motion controller: 1-off, 2-ON for x axis
# If someone messed with the controller manually(changed switch at the back), some values has to be changed
# code bellow is for 5 LEDs setup
import serial
from capture_spectra import *
from MAX14662 import *
from log_iv_t import *

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    write_timeout= 1,
    xonxoff=False,
    rtscts=False,
    dsrdtr=False)


class MOX06XXX:
    nm_LEDs = 0                 # number of LEDs in test setup (programmed for max 5 for now)


    def __init__(self, nm_LED):
        self.nm_LEDs = nm_LED

    def calibrate(self):
        print("Transition Stage Connection:")
        ser.write(b'?R\r\n')
        print(ser.readline().decode('utf-8'))
        time.sleep(.16)
        ser.write(b'V255\r\n')
        ser.readline()
        time.sleep(.16)
        ser.write(b'HX0\r\n')
        ser.readline()
        time.sleep(.16)
        ser.readline()
        ser.readline()

    def first_loop(self):
        turn.switch_off()
        int_time = 1
        counter = 0
        save_spec(int_time, "Dark")

        for i in range(self.nm_LEDs):
            time.sleep(1)
            ser.write(b'X+6420\r\n')
            ser.readline()
            time.sleep(.16)
            counter = counter + 1

            if counter == 1:
                turn.switch1()
                save_spec(int_time, "LED1")
                saveiv_t(pac_addr, adc_addr, "LED1")
            elif counter == 2:
                turn.switch2()
                save_spec(int_time, "LED2")
                saveiv_t(pac_addr, adc_addr, "LED2")
            elif counter == 3:
                turn.switch3()
                save_spec(int_time, "LED3")
                saveiv_t(pac_addr, adc_addr, "LED3")
            elif counter == 4:
                turn.switch4()
                save_spec(int_time, "LED4")
                saveiv_t(pac_addr, adc_addr, "LED4")
            elif counter == 5:
                turn.switch5()
                save_spec(int_time, "LED5")
                saveiv_t(pac_addr, adc_addr, "LED5")

        time.sleep(1)
        ser.write(b'HX0\r\n')
        ser.readline()



    def create_loop(self):
        int_time = .50
        counter = 0
        save_spec(int_time, "Dark")

        for i in range(self.nm_LEDs):
            time.sleep(1)
            ser.write(b'X+6420\r\n')
            ser.readline()
            time.sleep(.16)
            counter = counter + 1

            if counter == 1:
                save_spec(int_time, "LED1")
                saveiv_t(pac_addr, adc_addr, "LED1")
            elif counter == 2:
                save_spec(int_time, "LED2")
                saveiv_t(pac_addr, adc_addr, "LED2")
            elif counter == 3:
                save_spec(int_time, "LED3")
                saveiv_t(pac_addr, adc_addr, "LED3")
            elif counter == 4:
                save_spec(int_time, "LED4")
                saveiv_t(pac_addr, adc_addr, "LED4")
            elif counter == 5:
                save_spec(int_time, "LED5")
                saveiv_t(pac_addr, adc_addr, "LED5")

        time.sleep(1)
        ser.write(b'HX0\r\n')
        ser.readline()

    def start_test(self):
        self.calibrate()
        print("Test running.....")
        self.first_loop()
        while True:
            self.create_loop()


transition = MOX06XXX(1)
transition.start_test()
