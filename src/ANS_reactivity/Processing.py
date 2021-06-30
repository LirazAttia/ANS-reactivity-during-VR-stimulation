
### Missing: dealing with nans and inf, valueerrors, typeerrors
import numpy as np
import pandas as pd
from pathlib import Path
import neurokit2 as nk
import heartpy as hp
from pandas.core.frame import DataFrame
pd.options.mode.use_inf_as_na = True

BAD_TYPE_MESSAGE = "Invalid input: ({value})! Only pathlib.Path and strings are accepted."
DIRECTORY_NOT_EXISTING_MESSAGE = "Invalide input: ({value})! Directory doesn't exist."
HAVE_TO_BE_TUPLE_MESSAGE = "Invalid input: ({value})! Have to be tuple"
TUPLE_LENGTH_MESSAGE  = "Invalid input: Length mismatch: lenght of tuple must be 3 (not {value})."
TUPLE_SUM_MESSAGE = "Invalid input: The sum of the values must be 1 (not {value})."
TUPLE_NEGATIVE_MESSAGE = "Invalid input: ({value})! tuple values must be positive."
VALUES_ARE_NOT_NUMBERS_MESSAGE = "Invalid input: ({value})! tuple values must be type int or float."

class OfflineAnalysisANS:
    """
    Base class for offline ANS measures' analysis objects.
    
    This class provides an "interface" for subclasses to implement which
    conforms with the larger data processing pipeline of this project.
    """

    def __init__(self, data_path: str = r"ANS-reactivity-during-VR-stimulation\Data.csv", sample_rate: int = 512, time_window: int = 10, weights: tuple = (0.333, 0.333, 0.333)):
        pathlib_input = isinstance(data_path, Path)
        str_input = isinstance(data_path, str)
        if not (pathlib_input or str_input):
            raise TypeError(BAD_TYPE_MESSAGE.format(value=data_path))
        elif not Path(data_path).exists():
            raise ValueError(
                DIRECTORY_NOT_EXISTING_MESSAGE.format(value=data_path))
        else:
            self.data_path = data_path
        self.sample_rate = sample_rate
        self.time_window = time_window
        self.weights = weights
        self.n_samples = self.time_window*self.sample_rate
        
    def read_data(self) -> DataFrame:
        """ Pulling and reading the data into Dataframe.
        parm:
        return:
        """
        self.raw_data = pd.read_csv(self.data_path)

    
    def heart_rate(self):
        #Extracts heart rate from raw ECG data

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
            self.processed_data[column] = (self.processed_data[column]-min)/max
        self.normal_data = self.processed_data.copy()


    def score_adding(self, wights: tuple = (0.333, 0.333, 0.334)) -> DataFrame:
        """ making an index according to wights.
        parm:
        return:
        """
        if not isinstance(wights, tuple):
            raise TypeError(HAVE_TO_BE_TUPLE_MESSAGE.format(value=wights))
        elif len(wights) != 3:
            raise ValueError(TUPLE_LENGTH_MESSAGE.format(value=len(wights)))
        elif not (isinstance(wights[0], (int, float)) and isinstance(wights[1], (int, float)) and isinstance(wights[2], (int, float))):
            raise TypeError(VALUES_ARE_NOT_NUMBERS_MESSAGE.format(value=wights))
        elif sum(list(wights)) != 1:
            raise ValueError(TUPLE_SUM_MESSAGE.format(value=sum(list(wights))))
        elif not (wights[0] >=0 and wights[1] >=0 and wights[2] >=0):
            raise ValueError(TUPLE_NEGATIVE_MESSAGE.format(value=wights))
        else:
            self.normal_data["Fear_Index"] = self.normal_data["ECG"]*wights[0] + self.normal_data["GSR"]*wights[1] + self.normal_data["RESP"]*wights[2]
            self.scored_data = self.normal_data.copy()

    #def_plot_stress_score()