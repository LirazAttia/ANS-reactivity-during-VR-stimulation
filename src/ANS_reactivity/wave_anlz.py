from offline_processing import *
import numpy as np
import pandas as pd
import soundfile as sf
import matplotlib.pyplot as plt


def read_wav(wav_path: Path = r"C:\Users\Anthony\Desktop\backups\PublicSpeaking.wav"):
    """ """
    wav_list = []
    data, sr = sf.read(wav_path)
    wav_list.append(data)
    wav_data = pd.Series(wav_list[0], name = "Sound")
    wav_data = wav_data[0:38500000]
    return wav_data

def short_wav(wav_data: pd.Series , avg_chunk: int = 4096/2):
    """ """
    processes_wav_data = wav_data.groupby(np.arange(len(wav_data))//avg_chunk).mean().copy()
    return processes_wav_data
    
def plot_wav(processes_wav_data):
    """ """
    processes_wav_data.plot()
    plt.show()

def avg_chunk_creator(raw_data: DataFrame, wav_data: pd.Series):
    """ """
    wav_length = wav_data.size
    df_length = raw_data["GSR"].size
    avg_chunk = wav_length/df_length
    return avg_chunk

def merge_all_data(raw_data: DataFrame, processes_wav_data: pd.Series):
    """ """
    all_data = raw_data.copy()
    all_data["WAV"] = processes_wav_data
    print(all_data)
    return all_data

def correlation_creator(column1: pd.Series, column2: pd.Series,):
    """ """
    correlation = column1.corr(column2)
    return correlation




if __name__ == "__main__":

    data = OfflineAnalysisANS(data_path = r"C:\Users\Anthony\Desktop\Hackathon\ANS-reactivity-during-VR-stimulation\Data.csv")
    data.read_data()
    #data.process_samples()
    #data.normalizing_values()
    #data.score_adding()
    #data.scored_data()
    #print(data.raw_data["GSR"])

    wav_data = read_wav()
    avg_chunk = avg_chunk_creator(data.raw_data, wav_data)
    processes_wav_data = short_wav(wav_data, avg_chunk)
    plot_wav(processes_wav_data)
    all_data = merge_all_data(data.raw_data, processes_wav_data)

    print(correlation_creator(all_data["ECG"], all_data["WAV"]))
    print(correlation_creator(all_data["GSR"], all_data["WAV"]))
    print(correlation_creator(all_data["RESP"], all_data["WAV"]))
    print(correlation_creator(all_data["TIME"], all_data["WAV"]))
    print(correlation_creator(all_data["GSR"], all_data["ECG"]))
    print(correlation_creator(all_data["GSR"], all_data["RESP"]))
    print(correlation_creator(all_data["RESP"], all_data["ECG"]))




    

    
