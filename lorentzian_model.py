# Lorentzian model for finding spectral peaks, wavelength
from lmfit.models import *
import peakutils
import numpy as np
import numpy
from peakutils.plot import plot as pplot
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib import pyplot
from numpy import genfromtxt
import glob
import pandas as pd
#from capture_spectra import *


class lorentzian_2peaks:                # used for white LEDs, might break for blue/red/IR LEDs

    def __init__(self,                  # input parameters
                 spec_data,             # ndarray, spectra(unfiltered or filtered), goes in Y axis
                 wls,                   # ndarray, wavelength data, goes in X axis
                 distance,              # distance between peaks
                 threshold,             # float between [0., 1.], Normalized threshold. Only the peaks with amplitude higher than the threshold will be detected
                 interpolation_window,  # Number of points (before and after) each peak index to pass to func in order to increase the resolution in x
                 first_window,          # number of data points before and after first initial peak to feed into model
                 second_window,         # number of data points before and after second initial peak to feed into model
                 first_peak_sigma,      # change value if model breaks(usually value "5" works
                 second_peak_sigma):    # change value if model breaks(usually value "5" works

        self._spec_data = spec_data
        self._wls = wls
        self._distance = distance
        self._threshold = threshold
        self._interpolation_window = interpolation_window
        self._first_window = first_window
        self._second_window = second_window
        self._first_peak_sigma = first_peak_sigma
        self._second_peak_sigma = second_peak_sigma

    def initial_peak(self):
        index = peakutils.peak.indexes(self._spec_data, thres= self._threshold, min_dist= self._distance)
#        print("X index:", self._wls[index], "\nY index:", self._spec_data[index])
        return index

    def interpolate_initial_peak(self):
        interpolated_y_value = peakutils.interpolate(self._wls, self._spec_data,
                                                     ind=self.initial_peak(),
                                                     width= self._interpolation_window )

        print("Initial Interpolated peaks(AUD):", interpolated_y_value)
        return interpolated_y_value

    def windowing(self):
        first_range_left = int(self.initial_peak()[0] - self._first_window)
        first_range_right = int(self.initial_peak()[0] + self._first_window +1)
        first_xData = np.array(self._wls[first_range_left:first_range_right])
        first_yData = np.array(self._spec_data[first_range_left:first_range_right])

        second_range_left = int(self.initial_peak()[1] - self._second_window)
        second_range_right = int(self.initial_peak()[1] + self._second_window +1)
        second_xData = np.array(self._wls[second_range_left:second_range_right])
        second_yData = np.array(self._spec_data[second_range_left:second_range_right])

        return [first_xData, first_yData, second_xData, second_yData]  # I should find a better way, somehing like creating class here and making those attributes instead of returning a list


    def lorentzian_model(self):
        first_gmodel = LorentzianModel()
        first_params = first_gmodel.make_params(cen = self._wls[self.initial_peak()[0]],
                                                amp = self._spec_data[self.initial_peak()[0]],
                                                wid = self._first_window,
                                                sigma = self._first_peak_sigma)
        first_result = first_gmodel.fit(self.windowing()[1],
                                        first_params,
                                        x = self.windowing()[0])
#        print(first_result.fit_report())
#        print(first_result.values['height'])
#        print(first_result.values['center'])

        second_gmodel = LorentzianModel()
        second_params = second_gmodel.make_params(cen = self._wls[self.initial_peak()[1]],
                                                  amp = self._spec_data[self.initial_peak()[1]],
                                                  wid = self._second_window,
                                                  sigma = self._second_peak_sigma)
        second_result = second_gmodel.fit(self.windowing()[3],
                                          second_params,
                                          x = self.windowing()[2])
#        print(second_result.fit_report())
#        print(second_result.values['height'])
#        print(second_result.values['center'])


        return [first_result, second_result, first_result.values['height'],
                first_result.values['center'], second_result.values['height'],
                second_result.values['center'] ]

    def plot_lorentzian_spec(self):
        self.lorentzian_model()[0].plot_fit()
        self.lorentzian_model()[1].plot_fit()
        pplot(self._wls, self._spec_data, self.initial_peak())
        pyplot.title('Lorentzian Model')
        pyplot.ylabel('Amplitude(AUD)')
        pyplot.xlabel('Wavelength(nm)')
        plt.legend(loc='best')
        pyplot.show()



class lorentzian_1peak:
    def __init__(self,                  # input parameters
                 spec_data,             # ndarray, spectra(unfiltered or filtered), goes in Y axis
                 wls,                   # ndarray, wavelength data, goes in X axis
                 distance,              # distance between peaks
                 threshold,             # float between [0., 1.], Normalized threshold. Only the peaks with amplitude higher than the threshold will be detected
                 interpolation_window,  # Number of points (before and after) each peak index to pass to func in order to increase the resolution in x
                 first_window,          # number of data points before and after first initial peak to feed into model
                 first_peak_sigma):     # change value if model breaks(usually value "5" works


        self._spec_data = spec_data
        self._wls = wls
        self._distance = distance
        self._threshold = threshold
        self._interpolation_window = interpolation_window
        self._first_window = first_window
        self._first_peak_sigma = first_peak_sigma


    def initial_peak(self):
        index = peakutils.peak.indexes(self._spec_data, thres=self._threshold, min_dist=self._distance)
        #        print("X index:", self._wls[index], "\nY index:", self._spec_data[index])
        return index

    def interpolate_initial_peak(self):
        interpolated_y_value = peakutils.interpolate(self._wls, self._spec_data,
                                                     ind=self.initial_peak(),
                                                     width=self._interpolation_window)

        print("Initial Interpolated peaks(AUD):", interpolated_y_value)
        return interpolated_y_value

    def windowing(self):
        first_range_left = int(self.initial_peak()[0] - self._first_window)
        first_range_right = int(self.initial_peak()[0] + self._first_window + 1)
        first_xData = np.array(self._wls[first_range_left:first_range_right])
        first_yData = np.array(self._spec_data[first_range_left:first_range_right])


        return [first_xData, first_yData]  # I should find a better way, somehing like creating class here and making those attributes instead of returning a list

    def lorentzian_model(self):
        first_gmodel = LorentzianModel()
        first_params = first_gmodel.make_params(cen=self._wls[self.initial_peak()[0]],
                                                amp=self._spec_data[self.initial_peak()[0]],
                                                wid=self._first_window,
                                                sigma=self._first_peak_sigma)
        first_result = first_gmodel.fit(self.windowing()[1],
                                        first_params,
                                        x=self.windowing()[0])
        #print(first_result.fit_report())
        #        print(first_result.values['height'])
        #        print(first_result.values['center'])
        return [first_result, first_result.values['height'], first_result.values['center']]


    def plot_lorentzian_spec(self):
        self.lorentzian_model()[0].plot_fit()
        pplot(self._wls, self._spec_data, self.initial_peak())
        pyplot.title('Lorentzian Model')
        pyplot.ylabel('Amplitude(AUD)')
        pyplot.xlabel('Wavelength(nm)')
        plt.legend(loc='best')
        pyplot.show()



# test_run = lorentzian_1peak(          #np.array(get_spectra(0.05)),
#                                       genfromtxt("/home/pi/PycharmProjects/LED_Test_all/output/LED1/spec_1614768646.csv", delimiter=','),
#                                       genfromtxt("/home/pi/PycharmProjects/LED_Test_all/output/WLS/wls.csv", delimiter=','),
#                                       500,
#                                       .5,
#                                       80,
#                                       50,
#                                       20,)
                 # spec_data,             # ndarray, spectra(unfiltered or filtered), goes in Y axis
                 # wls,                   # ndarray, wavelength data, goes in X axis
                 # distance,              # distance between peaks
                 # threshold,             # float between [0., 1.], Normalized threshold. Only the peaks with amplitude higher than the threshold will be detected
                 # interpolation_window,  # Number of points (before and after) each peak index to pass to func in order to increase the resolution in x
                 # first_window,          # number of data points before and after first initial peak to feed into model
                 #* second_window,         # number of data points before and after second initial peak to feed into model
                 # first_peak_sigma,      # change value if model breaks(usually value "5" works
                 #* second_peak_sigma):    # change value if model breaks(usually value "5" works


#test_run.plot_lorentzian_spec()
#print(test_run.lorentzian_model())



def save_peaks(path, folder1, folder2):

    counter = 0
    df = pd.DataFrame()
    li = np.array([])
    ti = np.array([])
    wi = np.array([])
    for fname in sorted(glob.glob(path)):
        specf = fname

        test_run = lorentzian_1peak(  # np.array(get_spectra(0.05)),
            genfromtxt(specf),
            genfromtxt("/home/pi/PycharmProjects/LED_Test_all/output/WLS/wls.csv"),
            500,
            .5,
            80,
            50,
            60,)

#        print(fname)
        timestamp = str(fname.split('.')[0].split('_')[3])
        print(timestamp)
        ti = np.append(ti, timestamp)
        li = np.append(li, test_run.lorentzian_model()[1] )
        wi = np.append(wi, test_run.lorentzian_model()[2])
        print(test_run.lorentzian_model()[2])
        counter = counter + 1
        print(int(counter / 549) * 100, '%')
    ti = ti.astype(np.int)
    fi = np.concatenate((ti.reshape(-1, 1), li.reshape(-1, 1), wi.reshape(-1, 1)), axis=1)
    df = pd.DataFrame(fi)
    print(df)
    df.to_csv('/home/pi/PycharmProjects/LED_Test_all/output/'+folder1+'/'+folder2+'/peaks.csv', header=False, index=False)



#save_peaks(r"/home/pi/PycharmProjects/LED_Test_all/output/LED4/*.csv", "lorentzian_peaks_without_filter", "LED4")


