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