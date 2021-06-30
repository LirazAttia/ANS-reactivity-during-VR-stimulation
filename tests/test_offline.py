import pathlib

import pytest

from Processing import *

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
    assert len(self.GSR) == len(self.raw_data)/self.n_samples