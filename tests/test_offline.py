import pathlib

import pytest

from Processing import *

def test_wrong_input_type():
    fname = 2
    with pytest.raises(TypeError):
        q = OfflineAnalysisANS(pathlib.Path(fname))

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