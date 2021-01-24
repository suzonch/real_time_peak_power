import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import warnings
from scipy.optimize import differential_evolution
from numpy import genfromtxt
from peakutils.plot import plot as pplot
import peakutils


class raman_model:

    def __init__(self,                  # input parameters
                 spec_data,             # ndarray, spectra(unfiltered or filtered), goes in Y axis
                 wls,                   # ndarray, wavelength data, goes in X axis
                 distance,              # distance between peaks
                 threshold,             # float between [0., 1.], Normalized threshold. Only the peaks with amplitude higher than the threshold will be detected
                 interpolation_window,  # Number of points (before and after) each peak index to pass to func in order to increase the resolution in x
                 first_window,          # number of data points before and after first initial peak to feed into model
                 second_window):        # number of data points before and after second initial peak to feed into model

        self._spec_data = spec_data
        self._wls = wls
        self._distance = distance
        self._threshold = threshold
        self._interpolation_window = interpolation_window
        self._first_window = first_window
        self._second_window = second_window

    # Double Lorentzian peak function
    # bounds on parameters are set in generate_Initial_Parameters() below
    def double_Lorentz(self, x, a, b, A, w, x_0, A1, w1, x_01):

        return a * x + b + (2 * A / np.pi) * (w / (4 * (x - x_0) ** 2 + w ** 2)) + (2 * A1 / np.pi) * (
                w1 / (4 * (x - x_01) ** 2 + w1 ** 2))

    def sumOfSquaredError(self, parameterTuple):
        warnings.filterwarnings("ignore")  # do not print warnings by genetic algorithm

        return np.sum((self.windowing()[1] - self.double_Lorentz(self.windowing()[0], * parameterTuple)) ** 2)

    def generate_Initial_Parameters(self):
        print('testx')
        # min and max used for bounds
        maxX = max(self.windowing()[0])
        minX = min(self.windowing()[0])
        maxY = max(self.windowing()[1])
        minY = min(self.windowing()[1])

        test = 50
#        if maxY > 33500:
#            test = 40

        parameterBounds = []
        parameterBounds.append([-1.0, 1.0])  # parameter bounds for a
        parameterBounds.append([maxY / -2.0, maxY / 2.0])  # parameter bounds for b
        # change parameter
        parameterBounds.append([0.0, maxY * test])  # parameter bounds for A
        parameterBounds.append([0.0, maxY / 2.0])  # parameter bounds for w
        parameterBounds.append([minX, maxX])  # parameter bounds for x_0
        parameterBounds.append([0.0, maxY * test])  # parameter bounds for A1
        parameterBounds.append([0.0, maxY / 2.0])  # parameter bounds for w1
        parameterBounds.append([minX, maxX])  # parameter bounds for x_01

        # "seed" the numpy random number generator for repeatable results
        result = differential_evolution(self.sumOfSquaredError, parameterBounds, seed=3)
        return result.x

    def initial_peak(self):
        index = peakutils.peak.indexes(self._spec_data,
                                       thres= self._threshold,
                                       min_dist= self._distance)
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

        return [first_xData, first_yData]  # I should find a better way, somehing like creating class here and making those attributes instead of returning a list

    def pass_data(self):
        print('test')
        self.initialParameters = self.generate_Initial_Parameters()    # generate initial parameter values
        print('test1')
        print(self.initialParameters)
        fittedParameters, pcov = curve_fit(self.double_Lorentz(),
                                           self.windowing()[0],
                                           self.windowing()[1],
                                           self.initialParameters)     # curve fit the test data
        a, b, A, w, x_0, A1, w1, x_01 = fittedParameters    # create values for display of fitted peak function
        y_fit = self.double_Lorentz(self.windowing()[0], a, b, A, w, x_0, A1, w1, x_01)
        print(max(y_fit))
        return y_fit


test = raman_model( genfromtxt("/home/suzon/Work/LED_tests/short_run/FYL-5014UWC1C-15/led1/0_filtered/filteredSpec_1556200954.csv"),
                    genfromtxt("/home/suzon/Work/LED_tests/short_run/FYL-5014UWC1C-15/led1/wls.csv"),
                    100,
                    .5,
                    50,
                    80,
                    20)

print(max(test.pass_data()))
