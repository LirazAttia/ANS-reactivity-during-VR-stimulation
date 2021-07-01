from Processing import *
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
from pandas.core.frame import DataFrame


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
    ax.set_ylabel('Stress_Score')
    ax.set_title('Real time Data')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim([0, 1.2])

def averaging_samples(row_data: DataFrame, n_samples_for_averging: int = 10) -> DataFrame:
    """ averaging serval sampels in each column.
    parm:
    return:
    """
    avg_data = row_data.groupby(np.arange(len(row_data))//n_samples_for_averging).mean() #####
    return avg_data

##########################################

my_gen = data_gen()
index = count()
x_width = 20
data_range = 1200
start_sample = 20
bar_colors = ["r", "k", "g", "b"]
labels = ["ECG", "GSR", "RESP" , "Stress_Score"]
fear_values = [0.5, 0.5, 0.5, 0.5]
x = np.arange(len(labels))
width = 0.35


if __name__ == "__main__":
    data = OfflineAnalysisANS(data_path = r"C:\Users\Anthony\Desktop\Hackathon\ANS-reactivity-during-VR-stimulation\Data.csv")
    data.read_data()
    data.process_samples()
    data.normalizing_values()
    data.score_adding()
    #data.scored_data()
    print(data.processed_data["GSR"])


    plt.ion()
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, fear_values, width, label='Stress_Score', color = bar_colors)
    plot_me()
    ax.bar_label(rects1)

    input("wait...")
    for i in range(1000):
        real_time_data = data.scored_data.iloc[i, :]
        print(real_time_data)
        plt.cla()
        fear_values = [real_time_data["ECG"], real_time_data["GSR"], real_time_data["RESP"], real_time_data["Stress_Score"]]
        rects1 = ax.bar(x - width/2, fear_values, width, label='Stress_Score', color = bar_colors)
        plot_me()
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.1)

