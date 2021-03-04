import warnings
from avaspec import *
from log_iv_t import *
import time
from array import array
import os.path
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt




AVS_Init(0)
print('Found %d devices' % AVS_GetNrOfDevices())
idtype = AvsIdentityType *1
devs = AVS_GetList(75, 0, idtype)
sn = str(devs[1].SerialNumber.decode('utf-8'))
dev_h = AVS_Activate(devs[1])
dev_cfg_t = DeviceConfigType
dev_cfg = AVS_GetParameter(dev_h, 63484, 0, dev_cfg_t)
pixel_count = dev_cfg[1].m_Detector_m_NrPixels
print('Pixel count: %d' % pixel_count)

def measure(integration_time):
        ret = AVS_UseHighResAdc(dev_h, True)
        measconfig = MeasConfigType
        measconfig.m_StartPixel = 0
        measconfig.m_StopPixel = pixel_count - 1
        measconfig.m_IntegrationTime = integration_time
        measconfig.m_IntegrationDelay = 0
        measconfig.m_NrAverages = int(5)
        measconfig.m_CorDynDark_m_Enable = 0 # nesting of types does NOT work!!
        measconfig.m_CorDynDark_m_ForgetPercentage = 0
        measconfig.m_Smoothing_m_SmoothPix = 0
        measconfig.m_Smoothing_m_SmoothModel = 0
        measconfig.m_SaturationDetection = 0
        measconfig.m_Trigger_m_Mode = 0
        measconfig.m_Trigger_m_Source = 0
        measconfig.m_Trigger_m_SourceType = 0
        measconfig.m_Control_m_StrobeControl = 0
        measconfig.m_Control_m_LaserDelay = 0
        measconfig.m_Control_m_LaserWidth = 0
        measconfig.m_Control_m_LaserWaveLength = 0.0
        measconfig.m_Control_m_StoreToRam = 0
        ret = AVS_PrepareMeasure(dev_h, measconfig)
        nummeas = int(1)
        # ret = AVS_MeasureCallback(globals.dev_handle, ctypes.addressof(callbackclass.callback(self, 0, 0)),
        # nummeas)
        scans = 0
        while (scans < nummeas):
            ret = AVS_Measure(dev_h, 0, 1)
            dataready = False
            while (dataready == False):
                dataready = (AVS_PollScan(dev_h) == True)
                time.sleep(0.001)
            if (dataready == True):
                scans = scans + 1
                ts = 0
                specData = []
                resp = AVS_GetScopeData(dev_h, ts, specData)
                ts = resp[0]
                for idx in range(pixel_count):
                     #specData[idx] = resp[1][idx]
                     specData.append(resp[1][idx])
                return specData
            scans = scans + 1




def save_spec(int_time, folder): #saves raw unfiltered spectra
    ts = time.time()
    with open(os.path.join('output/'+ folder, 'spec_%d.csv' %ts), 'w') as f:
        for i in get_spectra(int_time):
            f.write('%d\n' %i)
    return get_spectra(int_time)


def get_spectra(int_time): #get raw unfiltered spectra
    spec = measure(int_time)
    return spec

def plot_spec(time):
    plt.plot(get_spectra(time))
    plt.show()


#calibrate
#plot_spec()


seconds = 600
start = time.time()
end = start + seconds

# while True:
#     print("Test running, please don't remove the curtain or turn on light", end - time.time())
#     save_spec(0.08, "LED4")
#     saveiv_t(pac_addr, adc_addr, "LED4")
#     time.sleep(1)
#     if time.time() >= end:
#         raise  RuntimeError("Test Done")

#plot_spec(0.08)
#save_spec(0.08, "Dark")
