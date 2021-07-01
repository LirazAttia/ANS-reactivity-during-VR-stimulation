
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
    sample_rate = 'kjhig'
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

def test_processed_ECG_length(): ## ValueError: Length of values (86) does not match length of index (87)
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    assert len(q.processed_data["ECG"]) == len(q.raw_data)/q.n_samples

def test_processed_RESP_length(): ## ValueError: Length of values (86) does not match length of index (87)
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    assert len(q.processed_data["RESP"]) == len(q.raw_data)/q.n_samples

def test_processed_GSR_length(): ## ValueError: Length of values (86) does not match length of index (87)
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    assert len(q.processed_data["GSR"]) == len(q.raw_data)/q.n_samples

def test_processed_TIME_length(): ## ValueError: Length of values (86) does not match length of index (87)
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    assert len(q.processed_data["TIME"]) == len(q.raw_data)/q.n_samples

def test_normalizing_values_ECG_min(): ## ValueError: Length of values (86) does not match length of index (87)
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    q.normalizing_values()
    assert q.processed_data["ECG"].min() == 0

def test_normalizing_values_GSR_min(): ## ValueError: Length of values (86) does not match length of index (87)
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    q.normalizing_values()
    assert q.processed_data["GSR"].min() == 0

def test_normalizing_values_RESP_max(): ## ValueError: Length of values (86) does not match length of index (87)
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    q.normalizing_values()
    assert q.processed_data["RESP"].max() == 1

def test_normalizing_values_GSR_max(): ## ValueError: Length of values (86) does not match length of index (87)
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    q.normalizing_values()
    assert q.processed_data["GSR"].max() == 1

def test_change_weights_recive_only_dict():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    with pytest.raises(TypeError):
        weights_list = list([0.333, 0.333, 0.334])
        q.change_weights(wights=weights_list)
    
def test_change_weights_length_long():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    with pytest.raises(ValueError):
        weights_long = {"ECG": 0.333, "GSR": 0.333, "RESP": 0.334, "A": 0.5}
        q.change_weights(weights=weights_long)

def test_change_weights_length_empty():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    with pytest.raises(ValueError):
        empty_dict = {}
        q.change_weights(weights=empty_dict)

def test_change_weights_sum():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    with pytest.raises(ValueError):
        summing_weights = {"ECG": 0.2, "GSR": 0.3, "RESP": 0.1}
        q.change_weights(weights=summing_weights)

def test_change_weights_positive():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    with pytest.raises(ValueError):
        negative_weights = {"ECG": 0.8, "GSR": 0.3, "RESP": -0.1}
        q.change_weights(weights=negative_weights)

def test_change_weights_str():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    with pytest.raises(TypeError):
        str_weights = {"ECG": 0.7, "GSR": "0.3", "RESP": 0.1}
        q.change_weights(weights=str_weights)

def test_change_weights_keys():
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    with pytest.raises(ValueError):
        str_weights = {"ABC": 0.7, "GSR": 0.2, "RESP": 0.1}
        q.change_weights(weights=str_weights)

def test_score_adding_without_nans(): ## ValueError: Length of values (86) does not match length of index (87)
    fname = 'Data.csv'
    q = OfflineAnalysisANS(fname)
    q.read_data()
    q.process_samples()
    q.normalizing_values()
    assert self.scored_data[self.scored_data["Fear_Index"] == np.nan].size() == 0 #Need duble check