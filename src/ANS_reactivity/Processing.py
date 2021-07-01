
### Missing: dealing with nans and inf, valueerrors, typeerrors
import numpy as np
import pandas as pd
from pathlib import Path
import neurokit2 as nk
import heartpy as hp
from pandas.core.frame import DataFrame
import matplotlib.pyplot as plt
pd.options.mode.use_inf_as_na = True

BAD_PATH_TYPE_MESSAGE = "Invalid input: ({value})! Only pathlib.Path and strings are accepted as data_path."
DIRECTORY_NOT_EXISTING_MESSAGE = "Invalide input: ({value})! Directory doesn't exist."
WEIGHTS_LENGTH_MESSAGE = "Invalid input: ({value}). Lenght of dict must be 3."
BAD_KEYS_NAMES_MESSAGE = "Invalid input: ({value}). Weights' keys must be ['ECG', 'GSR', RESP']."
WEIGHTS_SUM_MESSAGE = "Invalid input: The sum of the values must be 1 (not {value})."
WEIGHTS_NEGATIVE_MESSAGE = "Invalid input: ({value})! weights values must be positive."
WEIGHTS_ARE_NOT_NUMBERS_MESSAGE = "Invalid input: ({value})! tuple values must be type int or float."
BAD_SAMPLE_RATE_TYPE_MESSAGE = "Invalid input: ({value})! Only ints are accepted as sample_rate."
BAD_TIME_WINDOW_TYPE_MESSAGE = "Invalid input: ({value})! Only ints are accepted as time_window."
BAD_WEIGHTS_TYPE_MESSAGE = "Invalid input: ({value})! Only dicts are accepted as weights."


class OfflineAnalysisANS:
    """
    Base class for offline ANS measures' analysis objects.
    
    This class provides an "interface" for subclasses to implement which
    conforms with the larger data processing pipeline of this project.
    """

    def __init__(self, data_path: str = r"ANS-reactivity-during-VR-stimulation\Data.csv", sample_rate: int = 512, time_window: int = 10, weights: dict = {'ECG': 1/3, 'GSR': 1/3, 'RESP': 1/3}):

        if not (isinstance(data_path, Path) or isinstance(data_path, str)):
            raise TypeError(BAD_PATH_TYPE_MESSAGE.format(value=data_path))
        elif not Path(data_path).exists():
            raise ValueError(
                DIRECTORY_NOT_EXISTING_MESSAGE.format(value=data_path))
        else:
            self.data_path = data_path

        if not isinstance(sample_rate, int):
            raise TypeError(BAD_SAMPLE_RATE_TYPE_MESSAGE.format(value=sample_rate))
        else:
            self.sample_rate = sample_rate

        if not isinstance(time_window, int):
            raise TypeError(BAD_TIME_WINDOW_TYPE_MESSAGE.format(value=sample_rate))
        else:
            self.time_window = time_window

        if not isinstance(weights, dict):
            raise TypeError(BAD_WEIGHTS_TYPE_MESSAGE.format(value=weights))
        elif len(weights) != 3:
            raise ValueError(WEIGHTS_LENGTH_MESSAGE. format(value=weights))
        elif list(weights.keys()) != ["ECG", "GSR", "RESP"]:
            raise ValueError(BAD_KEYS_NAMES_MESSAGE.format(value=list(weights.keys())))
        elif not (isinstance(weights["ECG"], (int, float)) and isinstance(weights["GSR"], (int, float)) and isinstance(weights["RESP"], (int, float))):
            raise TypeError(WEIGHTS_ARE_NOT_NUMBERS_MESSAGE.format(value=weights))
        elif sum(weights.values()) != 1:
            raise ValueError(WEIGHTS_SUM_MESSAGE.format(value=sum(weights.values())))
        elif not (weights["ECG"] >= 0 and weights["GSR"] >= 0 and weights["RESP"] >= 0):
            raise ValueError(WEIGHTS_NEGATIVE_MESSAGE.format(value=weights))
        else:
            self.weights = weights

        self.n_samples = self.time_window*self.sample_rate

    def read_data(self) -> DataFrame:
        """ Pulling and reading the data into Dataframe.
        parm:
        return:
        """
        self.raw_data = pd.read_csv(self.data_path)

    def change_weights(self, weights: dict = {'ECG': 1/3, 'GSR': 1/3, 'RESP': 1/3}):
        if not isinstance(weights, dict):
            raise TypeError(BAD_WEIGHTS_TYPE_MESSAGE.format(value=weights))
        elif len(weights) != 3:
            raise ValueError(WEIGHTS_LENGTH_MESSAGE. format(value=weights))
        elif list(weights.keys()) != ["ECG", "GSR", "RESP"]:
            raise ValueError(BAD_KEYS_NAMES_MESSAGE.format(value=list(weights.keys())))
        elif not (isinstance(weights["ECG"], (int, float)) and isinstance(weights["GSR"], (int, float)) and isinstance(weights["RESP"], (int, float))):
            raise TypeError(WEIGHTS_ARE_NOT_NUMBERS_MESSAGE.format(value=weights))
        elif sum(weights.values()) != 1:
            raise ValueError(WEIGHTS_SUM_MESSAGE.format(value=sum(weights.values())))
        elif not (weights["ECG"] >= 0 and weights["GSR"] >= 0 and weights["RESP"] >= 0):
            raise ValueError(WEIGHTS_NEGATIVE_MESSAGE.format(value=weights))
        else:
            self.weights = weights

    def heart_rate(self):
        # Extracts heart rate from raw ECG data

        number_of_chunks = (len(self.ecg))//self.n_samples
        heart_rate_for_every_chunk = np.zeros(number_of_chunks)
        for data_chunks in range(number_of_chunks):
            try:
                data_chunk = list(range(data_chunks*number_of_chunks , data_chunks*number_of_chunks+self.n_samples))
                _, measures = hp.process(self.raw_data[data_chunk, 'ECG'])
                bpm_measured = measures['bpm']
                heart_rate_for_every_chunk[data_chunks] = bpm_measured
            except:
                if data_chunks == 0:
                    heart_rate_for_every_chunk[data_chunks] = np.NaN
                else:
                    heart_rate_for_every_chunk[data_chunks] = heart_rate_for_every_chunk[data_chunks-1]

        return heart_rate_for_every_chunk

    def resp_rate(self):
        # Extracts breathing rate from raw respiration data
        rsp_cleaned = nk.rsp_clean(self.resp)
        rsp_rate = nk.rsp_rate(rsp_cleaned, sampling_rate = self.sample_rate, window = self.time_window)
        return rsp_rate

    def process_samples(self) -> DataFrame:
        """ averaging serval sampels in each column.
        param:
        returns:
        """
        self.time = self.raw_data["TIME"]
        self.ecg = self.raw_data["ECG"]
        self.resp = self.raw_data["RESP"]
        self.gsr = self.raw_data["GSR"]

        self.processed_data = pd.DataFrame(
            columns=["TIME", "ECG", "RESP", "GSR"])

        self.processed_data["TIME"] = self.time.iloc[0:-1:self.n_samples] #Not sure this is correct, the basic idea is marking each "time-frame" according to start-time
        self.processed_data["ECG"] = self.heart_rate()
        self.processed_data["RESP"] = self.resp_rate()
        self.processed_data["GSR"] = self.gsr.groupby(np.arange(len(self.gsr))//self.n_samples).mean()

    def normalizing_values(self, columns_list=["ECG", "GSR", "RESP"]) -> DataFrame:
        """ normalazing each column.
        parm:
        return:
        """
        for column in columns_list:
            min = self.processed_data[column].min()
            max = self.processed_data[column].max()
            try:
                self.processed_data[column] = (self.processed_data[column]-min)/max
            except ValueError:
                max = 1 #### ?
                self.processed_data[column] = (self.processed_data[column]-min)/max
            finally:
                self.normal_data = self.processed_data.copy()

    def score_adding(self):
        """ making an index according to wights.
        parm:
        return:
        """
        self.normal_data["Stress_Score"] = self.normal_data["ECG"]*self.weights["ECG"] + self.normal_data["GSR"]*self.weights["GSR"] + self.normal_data["RESP"]*self.weights["RESP"]
        self.scored_data = self.normal_data.copy()

        def plot_score():
            """ """
            self.scored_data["Fear_Index"].plot()
            plt.title("Score")
            plt.xlabel("Samples")
            plt.ylabel("Fear_Score")   
            plt.show()