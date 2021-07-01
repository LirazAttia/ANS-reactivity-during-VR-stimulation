from Processing import OfflineAnalysisANS

class OnlineAnalysisANS(OfflineAnalysisANS):

    def __init__(self, data_path: str = r"ANS-reactivity-during-VR-stimulation\Data.csv", sample_rate: int = 512, time_window: int = 10, weights: dict = {'ECG': 1/3, 'GSR': 1/3, 'RESP': 1/3}):
        super().__init__( data_path, sample_rate, weights)
        self.time_window = (current_sample_data.loc[-1, 'TIME'] - current_sample_data.loc[o, 'TIME'])/1000
        
    def append_online_data_to_dataframe(online_data, current_sample_data):
        """
        This function appends new online data to the previouse data that was assesed in the current time_window.
        """
        current_sample_data = current_sample_data.append(new_data, ignore_index=True)

    def translate_online_data_to_csv(online_data):
        """
        This function combines all data in current time window to one csv, so that all ohter functions can work well.
        """
        # convert online_data as .cnt data to 4 integers, one for each data-type(TIME, ECG, GSR, RESP)

        current_sample_data = pd.Dataframe({'TIME':[], 'ECG': [], 'GSR': [], 'RESP': []})
        new_data = {'TIME': online_data[0], 'ECG':online_data[1], 'GSR':online_data[2], 'RESP':online_data[3]}
        while True:
            append_online_data_to_dataframe(online_data, current_sample_data)
        
        self.current_sample_data.to_csv('current_time_window_data.csv')
        return self.current_sample_data

    def read_data(self):
        self.raw_data = super().read_data(current_time_window_data)

    def heart_rate(self):
        heart_rate_for_every_chunk = super().heart_rate()

    def process_samples(self):
        self.processed_data = super().processed_data()

    def normalizing_values(self, columns_list=["ECG", "GSR", "RESP"])
        self.normal_data = super().normalizing_values()

    def score_adding(self):
        self.scored_data = super().score_adding()

    def resp_rate(self) -> pd.DataFrame:
        rsp_rate_avg = super().resp_rate()

    