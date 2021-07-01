from Processing import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import time

class OnlineAnalysisANS(OfflineAnalysisANS):

    def compute_data_for_simulation(self, data_path  = r"C:\Users\Anthony\Desktop\Hackathon\ANS-reactivity-during-VR-stimulation\Data.csv"):
        """ """
        data = OfflineAnalysisANS(data_path)
        data.read_data()
        data.process_samples()
        data.normalizing_values()
        data.score_adding()
        bar_data = data.scored_data
        return bar_data

        
    def plot_me(labels = ["ECG", "GSR", "RESP", "Stress_Score"],
    bar_colors = ["r", "k", "g", "b"],
    fear_values = [0.5, 0.5, 0.5, 0.5],
    x_positions = [0., 0.5, 1.0, 1.5],
    width = 0.15):
        """ """
        plt.ion()
        fig, ax = plt.subplots()
        rects1 = ax.bar(x_positions, fear_values, width, label='Stress_Score', color = bar_colors)
        plot_me()
        ax.bar_label(rects1)
        while True:
            ax.set_ylabel('Stress_Score')
            ax.set_title('Real time Data')
            ax.set_xticks(x_positions)
            ax.set_xticklabels(labels)
            ax.set_ylim([0, 1.2])
            yield fig, ax


    ##########################################

    def update_data_simulation(bar_data, 
    ax, 
    i,
    bar_colors = ["r", "k", "g", "b"],
    x_positions = [0., 0.5, 1.0, 1.5],
    width = 0.15):
        """ """
        real_time_data = bar_data.iloc[i, :]
        fear_values = [real_time_data["ECG"], real_time_data["GSR"], real_time_data["RESP"], real_time_data["Stress_Score"]]
        rects1 = ax.bar(x_positions, fear_values, width, label='Stress_Score', color = bar_colors)
        return rects1

    def bar_simulation(time_window: int = 10):
        """ """
        bar_data = compute_data_for_simulation()
        gen_plot = plot_me()
        fig, ax = next(gen_plot)

        for i in range(len(bar_data.index)):
            plt.cla()
            update_data_simulation(bar_data, ax, i)
            next(gen_plot)
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.1)



if __name__ == "__main__":
    a = OnlineAnalysisANS()
    a.bar_simulation()