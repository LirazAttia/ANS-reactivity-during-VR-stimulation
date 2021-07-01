from offline_processing import *
import numpy as np
import pandas as pd
import soundfile as sf
import matplotlib.pyplot as plt
import pathlib as Path 


def read_wav(wav_path: Path = r"C:\Users\Anthony\Desktop\backups\PublicSpeaking.wav"):
    """The function receives a path for a wav file and then converts it into a pd.Series and returns 
    the series if the data is relevant (without the last few minutes of silence)
        Input:  
        wav_path : Path - Path to the wave file 
        Output:
        wav_data : pd.Series - Series with the raw audio data      
    """
    wav_list = []
    data, _ = sf.read(wav_path)
    wav_list.append(data)
    wav_data = pd.Series(wav_list[0], name = "Sound")
    wav_data = wav_data[0:38500000]
    return wav_data

def short_wav(wav_data: pd.Series , avg_chunk: int = 4096/2):
    """
        This function matches the length of the wav_data to the general Dataframe by averaging according
        to the avg_chunk
        Input:
        wav_data : pd.Series - Series with the raw audio data
        avg_chunk : int - The conversion number adapting the legnths.
        Output:
        processes_wav_data: pd.Series - Series with the raw audio data after averaging.
        
    """
    processes_wav_data = wav_data.groupby(np.arange(len(wav_data))//avg_chunk).mean().copy()
    return processes_wav_data
    
def plot_wav(processes_wav_data):
    """
        This function plots the processed wav data 
        Input:
        processes_wav_data: pd.Series - Series with the raw audio data after averaging.  
        Output:
        None
        
    """
    processes_wav_data.plot()
    plt.show()

def avg_chunk_creator(raw_data: DataFrame, wav_data: pd.Series):
    """
        This function creates the conversion number that matches between the Dataframe and the pd.Series
        Input:
        raw_data : Dataframe - raw data of the stress measures 
        wav_data : pd.Series - Series with the raw audio data
        Output:
        avg_chunk : int - The conversion number adapting the legnths.
        
    """
    wav_length = wav_data.size
    df_length = raw_data["GSR"].size
    avg_chunk = wav_length/df_length
    return avg_chunk

def merge_all_data(raw_data: DataFrame, processes_wav_data: pd.Series):
    """
        This function converts the pd.Series and the Dataframe into one Dataframe
        The wav data is under the header WAV.
        Input:
        raw_data : Dataframe - raw data of the stress measures
        processes_wav_data: pd.Series - Series with the raw audio data after averaging.
        Output:
        all_data: Dataframe - The Dataframe after merging
    """
    all_data = raw_data.copy()
    all_data["WAV"] = processes_wav_data
    return all_data

def correlation_creator(column1: pd.Series, column2: pd.Series):
    """
        This function receives two columns with measures of either stress or audio data and returns the
        correlation between the two measures.
        Input:
        column1: pd.Series - The first measure 
        column2: pd.Series - The second measure
        Output:
        correlation: float - The correlation
        
    """
    correlation = column1.corr(column2)
    return correlation


if __name__ == "__main__":
    data = OfflineAnalysisANS(data_path = r"Data.csv")
    data.read_data()
    wav_data = read_wav()
    avg_chunk = avg_chunk_creator(data.raw_data, wav_data)
    processes_wav_data = short_wav(wav_data, avg_chunk)
    plot_wav(processes_wav_data)
    all_data = merge_all_data(data.raw_data, processes_wav_data)

    print("WAV and ECG correlation", correlation_creator(all_data["ECG"], all_data["WAV"]))
    print("WAV and ECG correlation",correlation_creator(all_data["GSR"], all_data["WAV"]))
    print("WAV and ECG correlation",correlation_creator(all_data["RESP"], all_data["WAV"]))






    

    
