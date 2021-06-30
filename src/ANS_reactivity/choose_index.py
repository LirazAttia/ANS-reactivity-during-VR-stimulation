from Processing import *
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from pandas.core.frame import DataFrame

def random_wights():
    """ """
    w1 = random.uniform(0, 1)
    w2 = random.uniform(0, 1 - w1) 
    w3 = 1 - (w2 + w1)
    wights_list = [w1,w2,w3]
    random.shuffle(wights_list)
    wights_tuple = tuple(wights_list)
    return wights_tuple

def index_trying(normal_data: DataFrame) -> DataFrame:
    """ making an index according to wights.
    parm:
    return:
    """
    wights = random_wights()
    print(wights)
    normal_data["Fear_Index"] = normal_data["ECG"]*wights[0] + normal_data["GSR"]*wights[1] +normal_data["RESP"]*wights[2]
    processed_data = normal_data.copy()
    std = processed_data["Fear_Index"].std()
    return std, wights

def std_collecting(normal_data: DataFrame, n_sample: int = 10000):
    """ """
    std_max, wights_max = 0, 0
    for n in range(n_sample):
        std, wights = index_trying(normal_data)
        print(std, wights)
        if std_max < std:
            std_max, wights_max = std, wights
    return std_max, wights_max




if __name__ == "__main__":
    row_data = read_data(data_path)
    print("Row data\n",row_data) ######
    avg_data = averaging_samples(row_data, n_samples_for_averging)
    #print("AVG data\n",avg_data) ######
    normal_data = normalizing_values(avg_data)

    std, wights = std_collecting(normal_data)
    print("STD: ", std, "WIGHTS: ", wights)
    #print("Normal data\n", normal_data)
    #for i in range(10):
    #processed_data = index_trying(normal_data)
    #print("Processed data\n",processed_data)