
import random
import numpy as np
from itertools import count
from numpy.core.records import array
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc
import numpy as np
import time
import matplotlib.pyplot as plt


def data_gen():
    while True:
        data_array = np.random.random(1)
        mean_array = np.nanmean(data_array) * 10
        yield mean_array

def axis_creator(y, x_width = 10):
    y_vals = next(my_gen)
    y = y.tolist()
    y.append(y_vals)

    while len(y) > x_width:
        y.pop(0)

    y = np.array(y)
    print(x,y)
    return y


##########################################

my_gen = data_gen()
index = count()
x_width = 20
data_range = 120
start_sample = 20

#x = np.array([0])
#y = np.array([0])
x= np.linspace(start = 0, stop = x_width, num= x_width)
y = np.linspace(start = 0, stop = x_width, num= x_width)


#plt.style.use('fivethirtyeight')
#plt.figure(figsize=(14, 14))

plt.ion()

# here we are creating sub plots
figure, ax = plt.subplots(figsize=(8, 8))
line1, = ax.plot(x, y)
ax.set_ylim([0, x_width +0.5 * x_width])

# setting title
plt.title("Real Time Data", fontsize=20)

# setting x-axis label and y-axis label
plt.xlabel("X_Time")
plt.ylabel("Y_Fear Level")

for i in range(data_range):
    print("LOOP")
    y  = axis_creator(y, x_width)
    line1.set_xdata(x)
    line1.set_ydata(y)
    #figure.tight_layout()
    figure.canvas.draw()
    figure.canvas.flush_events()
    time.sleep(0.1)

print("Finish")
