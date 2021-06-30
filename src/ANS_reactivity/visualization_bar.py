
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
        mean_array = np.nanmean(data_array) * 100
        yield mean_array

def value_creator(y):
    y = [next(my_gen), next(my_gen), next(my_gen)]
    #y = np.array(y)
    return y

def plot_me():
    ax.set_ylabel('Fear_Level')
    ax.set_title('Real time Data')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim([0, 100])



##########################################

my_gen = data_gen()
index = count()
x_width = 20
data_range = 1200
start_sample = 20
bar_colors = ["r", "k", "g"]



labels = ['HR', 'GSR', 'RR']
fear_values = [50, 50, 30]
#women_means = [25, 32, 34, 20, 25]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

plt.ion()
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, fear_values, width, label='Fear_Level', color = bar_colors)
#rects2 = ax.bar(x + width/2, women_means, width, label='Women')

# Add some text for labels, title and custom x-axis tick labels, etc.
plot_me()
#ax.legend()

ax.bar_label(rects1)#, padding=3)
#ax.bar_label(rects2, padding=3)

#fig.tight_layout()

for i in range(data_range):
    print("LOOP")
    plt.cla()
    fear_values = value_creator(fear_values)
    rects1 = ax.bar(x - width/2, fear_values, width, label='Fear_Level', color = bar_colors)
    plot_me()
    #y  = axis_creator(y, x_width)
    #line1.set_xdata(measurement_labels)
    #ax.set_yscale(y)
    #figure.tight_layout()
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.5)

