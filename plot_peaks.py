from numpy import genfromtxt
import numpy as np
import numpy
import matplotlib.pyplot as plt
from scipy import signal




s = genfromtxt("/home/pi/PycharmProjects/LED_Test_all/output/lorentzian_peaks_without_filter/LED1/peaks.csv", delimiter=',')

temp = genfromtxt("/home/pi/PycharmProjects/LED_Test_all/output/LED1/iv_t.csv",delimiter=',')

#temp = genfromtxt("/home/suzon/Work/LED_tests/short_run/MTE9440N/led1/temp_env.csv",delimiter=' ')



temperature = np.around([temp[:,3]], decimals=0)
temperature = temperature.astype(numpy.int64)
temperature = temperature.reshape(550)
# print(temperature)

v_drop = np.around([temp[:,2]], decimals=0)
v_drop = v_drop.astype(numpy.int64)
v_drop = v_drop.reshape(550)


time = s[:,0]
time = time - time[0]
time = time.astype(numpy.int64)
time = time.reshape(550)



amp = np.around([s[:,1]], decimals=2)
amplitude = amp.astype(numpy.int64)
amplitude = amplitude.reshape(550)


#amp2 = np.around([s[:,3]], decimals=0)
#amplitude2 = amp2.astype(numpy.int64)
#amplitude2 = amplitude2.reshape(110)


wav = np.around(s[:,2], decimals=3)
wav1 = wav.astype(numpy.int64)
#wav1 = wav1.reshape(550)

#b,a = signal.butter(3, 0.05)
#zi = signal.lfilter_zi(b,a)
#wav1, _ = signal.lfilter(b,a, wav1, zi = zi*wav1[0])

#wav2 = np.around(s[:,4], decimals=2)
#b,a = signal.butter(3, 0.09)
#zi = signal.lfilter_zi(b,a)
#wav2, _ = signal.lfilter(b,a, wav2, zi = zi*wav2[0])







def plot4(time, amplitude,v_drop,wav1, temp):
    def make_patch_spines_invisible(ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.values():
            sp.set_visible(False)

    fig, host = plt.subplots()
    fig.subplots_adjust(right=0.75)

    par1 = host.twinx()
    par2 = host.twinx()
    par3 = host.twinx()

    par2.spines["right"].set_position(("axes", 1.1))
    par3.spines["right"].set_position(("axes", 1.2))

    make_patch_spines_invisible(par2)
    make_patch_spines_invisible(par3)

    par2.spines["right"].set_visible(True)
    par3.spines["right"].set_visible(True)

    p1, = host.plot(time, amplitude, "b-", label="First peak AUD")
    p2, = par1.plot(time, v_drop, "r-", label="Voltage Drop")
    p3, = par2.plot(time, wav1, "g-", label="First Peak Wavelength")
    p4, = par3.plot(time, temp, "c-", label="Temperature")

    host.set_xlabel("Time(s)")
    host.set_ylabel("First peak (AUD)")
    par1.set_ylabel("Voltage Drop")
    par2.set_ylabel("First Peak Wavelength")
    par3.set_ylabel("Temperature")

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())
    par3.yaxis.label.set_color(p4.get_color())


#    tkw = dict(size=4, width=11)

    tkw = dict(size=4, width=1.5)

    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
    par3.tick_params(axis='y', colors=p4.get_color(), **tkw)
    host.tick_params(axis='x', **tkw)

    lines = [p1, p2, p3, p4]


    host.legend(lines, [l.get_label() for l in lines])
    plt.show()

def plot2(time, amplitude,wav1):
    def make_patch_spines_invisible(ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.values():
            sp.set_visible(False)

    fig, host = plt.subplots()
    fig.subplots_adjust(right=0.75)

    par1 = host.twinx()
    par2 = host.twinx()
#    par3 = host.twinx()

    par2.spines["right"].set_position(("axes", 1.1))
#    par3.spines["right"].set_position(("axes", 1.2))

    make_patch_spines_invisible(par2)
#    make_patch_spines_invisible(par3)

    par2.spines["right"].set_visible(True)
#    par3.spines["right"].set_visible(True)


    p1, = host.plot(time, amplitude, "b-", label="First peak AUD Uncontrolled")
#    p2, = par1.plot(time, amplitude2, "r-", label="Second peak AUD")
    p3, = par2.plot(time, wav1, "g-", label="First Peak Wavelength Uncontrolled")
#    p4, = par3.plot(time, wav2, "c-", label="Second peak Wavelength")

    host.set_xlabel("Time(s)")
    host.set_ylabel("First peak (AUD)")
#    par1.set_ylabel("Second peak (AUD)")
    par2.set_ylabel("First Peak Wavelength")
#    par3.set_ylabel("Second peak Wavelength")

    host.yaxis.label.set_color(p1.get_color())
#    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())
#    par3.yaxis.label.set_color(p4.get_color())

    tkw = dict(size=4, width=11)

    tkw = dict(size=4, width=1.5)

    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
#    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
#    par3.tick_params(axis='y', colors=p4.get_color(), **tkw)
    host.tick_params(axis='x', **tkw)

    lines = [p1, p3]


    host.legend(lines, [l.get_label() for l in lines])
    plt.show()



plot2(time, amplitude, wav1)
