import csv
import time
from lorentzian_model import *


def save_file():
    x_time = int(time.time())
    first_peak_aud = test_run.lorentzian_model()[0].values['height']
    first_peak_wav = test_run.lorentzian_model()[0].values['center']
    fieldnames = ['Timestamp', 'first_peak_aud', 'first_peak_wav']
    with open("//output/data.csv", 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    while True:
        with open("//output/data.csv", 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            test = lorentzian_2peaks(np.array(get_spectra(0.05)),
                                      genfromtxt("/home/suzon/Work/LED_tests/long_run/long_LTW/wls.csv"),
                                     50,
                                     .7,
                                     80,
                                     50,
                                     15,
                                     10,
                                     10)

            info = {
                "Timestamp": x_time,
                "first_peak_aud": first_peak_aud,
                "first_peak_wav": first_peak_wav
            }

            csv_writer.writerow(info)
            print(x_time, first_peak_aud, first_peak_wav)

            x_time =int(time.time())
            first_peak_aud = test.lorentzian_model()[0].values['height']
            first_peak_wav = test.lorentzian_model()[0].values['center']

        time.sleep(1)

save_file()
