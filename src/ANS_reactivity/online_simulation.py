from Processing import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import time

class OnlineAnalysisANS(OfflineAnalysisANS):
    """ """
    def __init__(self, data_path: str = r"C:\Users\Anthony\Desktop\Hackathon\ANS-reactivity-during-VR-stimulation\Data.csv", sample_rate: int = 512, time_window: int = 10, weights: dict = {'ECG': 1/3, 'GSR': 1/3, 'RESP': 1/3}):
        """ """
        OfflineAnalysisANS.__init__(self, data_path, sample_rate, time_window,  weights)

    def compute_data_for_simulation(self):
        """ """
        self.read_data()
        self.process_samples()
        self.normalizing_values()
        self.score_adding()

        
    def plot_me(self, labels = ["ECG", "GSR", "RESP", "Stress_Score"],
        bar_colors = ["r", "k", "g", "b"],
        fear_values = [0.5, 0.5, 0.5, 0.5],
        x_positions = [0., 0.5, 1.0, 1.5],
        width = 0.15):
        """ """
        plt.ion()
        fig, ax = plt.subplots()
        rects1 = ax.bar(x_positions, fear_values, width, label='Stress_Score', color = bar_colors)
        self.plot_me()
        ax.bar_label(rects1)
        while True:
            ax.set_ylabel('Stress_Score')
            ax.set_title('Real time Data')
            ax.set_xticks(x_positions)
            ax.set_xticklabels(labels)
            ax.set_ylim([0, 1.2])
            yield fig, ax

    def update_data_simulation(self, 
        ax, 
        i,
        bar_colors = ["r", "k", "g", "b"],
        x_positions = [0., 0.5, 1.0, 1.5],
        width = 0.15):
        """ """
        real_time_data = self.scored_data.iloc[i, :]
        fear_values = [real_time_data["ECG"], real_time_data["GSR"], real_time_data["RESP"], real_time_data["Stress_Score"]]
        rects1 = ax.bar(x_positions, fear_values, width, label='Stress_Score', color = bar_colors)
        return rects1

    def bar_simulation(self, loop_time: float = 0.1):
        """ """
        self.compute_data_for_simulation()
        gen_plot = self.plot_me()
        fig, ax = next(gen_plot)

        for i in range(len(self.scored_data.index)):
            plt.cla()
            self.update_data_simulation(ax, i)
            next(gen_plot)
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(loop_time)



if __name__ == "__main__":
    on_val = OnlineAnalysisANS()
    on_val.bar_simulation()