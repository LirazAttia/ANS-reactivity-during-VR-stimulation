from Processing import OfflineAnalysisANS

class OnlineAnalysisANS(OfflineAnalysisANS):

    def __init__(self, data_path: str = r"ANS-reactivity-during-VR-stimulation\Data.csv", sample_rate: int = 512, time_window: int = 10, weights: dict = {'ECG': 1/3, 'GSR': 1/3, 'RESP': 1/3}):
        self.
        
    def append_online_data_to_dataframe(online_data, current_sample_data):
        # ffff
        
        current_sample_data = 

        df_marks.append(new_row, ignore_index=True)

    def tranlate_online_data_to_csv(online_data):
        # convert online_data as .cnt data to 3 integers, one for each data-type(ECG, GSR, RESP)

