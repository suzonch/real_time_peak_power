# Lorentzian model for finding spectral peaks, wavelength
from lmfit.models import *
import peakutils
import numpy as np
from peakutils.plot import plot as pplot
from matplotlib import pyplot
from numpy import genfromtxt
from capture_spectra import *


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


        return [first_result, second_result]

    def plot_lorentzian_spec(self):
        self.lorentzian_model()[0].plot_fit()
        self.lorentzian_model()[1].plot_fit()
        pplot(self._wls, self._spec_data, self.initial_peak())
        pyplot.title('Lorentzian Model')
        pyplot.ylabel('Amplitude(AUD)')
        pyplot.xlabel('Wavelength(nm)')
        plt.legend(loc='best')
        pyplot.show()



test_run = lorentzian_2peaks(np.array(get_spectra(0.05)),
                                      genfromtxt("/home/pi/PycharmProjects/LED_Test_all/output/WLS/wls.csv", delimiter=','),
                                      50,
                                      .7,
                                      80,
                                      50,
                                      15,
                                      10,
                                      10)
                 # spec_data,             # ndarray, spectra(unfiltered or filtered), goes in Y axis
                 # wls,                   # ndarray, wavelength data, goes in X axis
                 # distance,              # distance between peaks
                 # threshold,             # float between [0., 1.], Normalized threshold. Only the peaks with amplitude higher than the threshold will be detected
                 # interpolation_window,  # Number of points (before and after) each peak index to pass to func in order to increase the resolution in x
                 # first_window,          # number of data points before and after first initial peak to feed into model
                 # second_window,         # number of data points before and after second initial peak to feed into model
                 # first_peak_sigma,      # change value if model breaks(usually value "5" works
                 # second_peak_sigma):    # change value if model breaks(usually value "5" works


# def test():
#     while True:
#         time.sleep(2)
#         return test_run.lorentzian_model()


#test_run.plot_lorentzian_spec()

