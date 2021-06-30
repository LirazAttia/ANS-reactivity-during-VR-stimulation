
### Missing: dealing with nans and inf, valueerrors, typeerrors
import numpy as np
import pandas as pd
from pathlib import Path
import neurokit2 as nk
import heartpy as hp

from pandas.core.frame import DataFrame

class OfflineAnalysisANS:
    """
    Base class for offline ANS measures' analysis objects.
    
    This class provides an "interface" for subclasses to implement which
    conforms with the larger data processing pipeline of this project.
    """


    def __init__(self, data_path: str = r"ANS-reactivity-during-VR-stimulation\Data.csv", sample_rate: int = 512, time_window: int = 10, weights: tuple = (0.333, 0.333, 0.333)):
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
        self.raw_data = pd.read_csv(self.path)

    
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
        rsp_rate = pd.Dataframe(nk.rsp_rate(rsp_cleaned, sampling_rate = self.sample_rate, window = self.time_window))
        rsp_rate_avg = rsp_rate.groupby(np.arange(len(rsp_rate))//self.n_samples).mean()
        return rsp_rate_avg

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
            columns=["time", "heart_rate", "resp_rate", "gsr"])

        n_samples = self.time_window*self.sample_rate
        
        self.processed_data["time"] = self.time.iloc[0:-1:n_samples] #Not sure this is correct, the basic idea is marking each "time-frame" according to start-time
        self.processed_data["heart_rate"] = heart_rate()
        self.processed_data["resp_rate"] = resp_rate()
        self.processed_data["gsr"] = self.gsr.groupby(np.arange(len(self.gsr))//n_samples).mean()

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


    def score_adding(self, wights: tuple = (0.333, 0.333, 0.333)) -> DataFrame:
        """ making an index according to wights.
        parm:
        return:
        """
        self.normal_data["Fear_Index"] = self.normal_data["ECG"]*wights[0] 
                                        + self.normal_data["GSR"]*wights[1] 
                                        + self.normal_data["RESP"]*wights[2]
        self.scored_data = self.normal_data.copy()



if __name__ == "__main__":

    row_data = read_data(data_path)
    print("Row data\n",row_data) ######
    avg_data = averaging_samples(row_data, n_samples_for_averging)
    print("AVG data\n",avg_data) ######
    normal_data = normalizing_values(avg_data)
    print("Normal data\n", normal_data)
    processed_data = index_adding(normal_data, wights)
    print("Processed data\n",processed_data)




