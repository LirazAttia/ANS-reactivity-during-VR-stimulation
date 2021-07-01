import pathlib
import numpy as np
import pandas as pd
import pytest

from Processing import * # I think its have to be in the same folder for this script recognize Processing

def test_wrong_input_type_path():
    fname = 2
    with pytest.raises(TypeError):
        q = OfflineAnalysisANS(fname)

def test_wrong_input_type_weigths():
    fname = 'Data.csv'
    weights = 2
    with pytest.raises(TypeError):
        q = OfflineAnalysisANS(fname, weights=weights)

def test_wrong_input_type_sample_rate():
    fname = 'Data.csv'
    sample_rates = 'kjhig'
    with pytest.raises(TypeError):
        q = OfflineAnalysisANS(fname, sample_rate=sample_rate)

def test_wrong_input_type_time_window():
    fname = 'Data.csv'
    time_window = 'kjhig'
    with pytest.raises(TypeError):
        q = OfflineAnalysisANS(fname, time_window=time_window)

def test_data_attr_is_df():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    assert isinstance(q.raw_data, pd.DataFrame)

def test_processed_HR_length():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.heart_rate()
    assert len(self.hr) == len(self.raw_data)/self.n_samples

def test_processed_RESP_length():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.resp_rate()
    assert len(self.resp) == len(self.raw_data)/self.n_samples

def test_processed_GSR_length():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    assert len(self.GSR) == len(self.raw_data)/self.n_samples

def test_processed_TIME_length():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    assert len(self.time) == len(self.raw_data)/self.n_samples

def test_normalizing_values_ECG_min():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    q.normalizing_values()
    assert self.processed_data["ECG"].min() == 0

def test_normalizing_values_GSR_min():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    q.normalizing_values()
    assert self.processed_data["GSR"].min() == 0

def test_normalizing_values_RESP_max():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    q.normalizing_values()
    assert self.processed_data["RESP"].max() == 1

def test_normalizing_values_GSR_max():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    q.normalizing_values()
    assert self.processed_data["GSR"].max() == 1

def test_score_adding_recive_only_tuple():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    q.normalizing_values()
    with pytest.raises(TypeError):
        wights_list = list([0.333, 0.333, 0.334])
        q.score_adding(wights = wights_list)
    
def test_score_adding_tuple_length_long():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    q.normalizing_values()
    with pytest.raises(ValueError):
        wights_long = (0.333, 0.333, 0.334, 0.5)
        q.score_adding(wights = wights_long)

def test_score_adding_tuple_length_empty():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    q.normalizing_values()
    with pytest.raises(ValueError):
        empty_tuple = tuple()
        q.score_adding(wights = empty_tuple)

def test_score_adding_tuple_sum_to_one():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    q.normalizing_values()
    with pytest.raises(ValueError):
        summing_tuple = (0.2, 0.3, 0.1)
        q.score_adding(wights = summing_tuple)

def test_score_adding_tuple_posetive():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    q.normalizing_values()
    with pytest.raises(ValueError):
        negative_tuple = (0.8, 0.3, -0.1)
        q.score_adding(wights = negative_tuple)

def test_score_adding_tuple_with_str():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    q.normalizing_values()
    with pytest.raises(TypeError):
        str_tuple = (0.7, "0.3", 0.1)
        q.score_adding(wights = str_tuple)

def test_score_adding_without_nans():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    q.normalizing_values()
    assert self.scored_data[self.scored_data["Fear_Index"] == np.nan].size() == 0 #Need duble check


