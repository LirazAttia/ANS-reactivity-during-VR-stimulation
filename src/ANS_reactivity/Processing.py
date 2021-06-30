
### Missing: dealing with nans and inf, valueerrors, typeerrors
import numpy as np
import pandas as pd
from pathlib import Path

from pandas.core.frame import DataFrame

# Defenitions
n_samples_for_averging : int = 100
wights: tuple = (0.333, 0.333, 0.333)
data_path = Path(r"C:\Users\Anthony\Desktop\extra\Data.csv")


#####################################################################################

class OfflineAnalysisANS:
    """
    Base class for offline ANS measures' analysis objects.
    
    This class provides an "interface" for subclasses to implement which
    conforms with the larger data processing pipeline of this project.
    """

    def read_data(self, data_path: Path) -> DataFrame:
        """ Pulling and reading the data into Dataframe.
        parm:
        return:
        """
        self.path = Path(data_path)
        self.raw_data = pd.read_csv(self.path)

    def heart_rate(ecg, n_samples):
        #Extracts heart rate from raw ECG data
        pass

    def resp_rate(breaths, n_samples):
        # Extracts breathing rate from raw respiration data
        pass

    def process_samples(self, n_samples: int = 10) -> DataFrame:
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
        
        self.processed_data["time"] = self.time.iloc[0:-1:n_samples] #Not sure this is correct, the basic idea is marking each "time-frame" according to start-time
        self.processed_data["heart_rate"] = heart_rate(self.ecg, n_samples)
        self.processed_data["resp_rate"] = resp_rate(self.resp, n_samples)
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




