import numpy as np
import pandas as pd
from pathlib import Path
import heartpy as hp

from pandas.core.frame import DataFrame

data = pd.read_csv('sympathetic_data.csv')


class OfflineAnalysisANS:

    def __init__(self, data_path: str = r"ANS-reactivity-during-VR-stimulation\Data.csv", sample_rate: int = 512, time_window: int = 10, weights: tuple = (0.333, 0.333, 0.333)):
        '''pathlib_input = isinstance(data_path, pathlib.Path)
        str_input = isinstance(data_path, str)
        if not (pathlib_input or str_input):
            raise TypeError(BAD_TYPE_MESSAGE.format(value=data_path))
        elif not pathlib.Path(data_path).exists():
            raise ValueError(
                DIRECTORY_NOT_EXISTING_MESSAGE.format(value=data_path))
        else:
            self.data_path = data_path'''
        self.sampe_rate = sample_rate
        self.data_path = data_path
        self.sample_rate = sample_rate
        self.time_window = time_window
        self.weights = weights
        self.n_samples = self.time_window*self.sample_rate
        self.ecg = data['ECG']

    def heart_rate(self):
        '''
        This function extracts the heart rate from ECG data.
        It has no input because it uses the data of the class. 
        Its output is a numpy array of beats per minute (bpm) for each time_window.

        Noisy ECG data that cannot produce a bpm output is ignored,
        and the previous time-window's bpm is refered to instead (unless the noise
        is in the first time window. In that case, the output of the bpm is NaN)
        '''

        number_of_chunks = (len(self.ecg))//self.n_samples
        heart_rate_for_every_chunk = np.zeros(number_of_chunks)
        for data_chunks in range(number_of_chunks):
            try:
                data_chunk = np.arange(data_chunks*self.n_samples, (data_chunks+1)*self.n_samples)
                relevant_data = self.ecg[data_chunk]
                relevant_data = relevant_data.reset_index(drop = True)

                working_data, measures = hp.process(relevant_data, self.sample_rate)
                bpm_measured = measures['bpm']
                if bpm_measured < 220:
                    heart_rate_for_every_chunk[data_chunks] = bpm_measured
                else:
                    raise Exception("")
            except:
                if data_chunks == 0:
                    heart_rate_for_every_chunk[data_chunks] = np.NaN
                else:
                    heart_rate_for_every_chunk[data_chunks] = heart_rate_for_every_chunk[data_chunks-1]

        return (heart_rate_for_every_chunk)


data = OfflineAnalysisANS('sympathetic_data.csv')
a = data.heart_rate()
print(type(a))
