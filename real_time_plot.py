from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

index = count()



def animate(i):
    data = pd.read_csv('//output/data.csv')
    x = data['Timestamp']
    y1 = data['first_peak_aud']
    y2 = data['first_peak_wav']

    plt.cla()

    plt.plot(x, y1, label='AUD')
    plt.plot(x, y2, label='Wavelength')

    plt.legend(loc='best')
#    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()
