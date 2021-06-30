import numpy as np
import pandas as pd
import matplotlib as plt
from pathlib import Path
from pandas.core.frame import DataFrame
from sklearn.decomposition import PCA
from processing import *





model = PCA(n_components=2)


#model.fit(X_iris)

#learning_model = PCA(n_components=2)


if __name__ == "__main__":

    row_data = read_data(data_path)
    print("Row data\n",row_data) ######
    avg_data = averaging_samples(row_data, n_samples_for_averging)
    print("AVG data\n",avg_data) ######
    normal_data = normalizing_values(avg_data)
    print("Normal data\n", normal_data)
    processed_data = index_adding(normal_data, wights)
    print("Processed data\n",processed_data)

    new_processed_data = processed_data[["ECG", "RESP"]]#, ]]
    new_processed_data = new_processed_data.dropna(axis= "index")

    learning_model = PCA(n_components=2)
    learning_model.fit(new_processed_data)  # notice how the labels aren't specified
    model_array = learning_model.transform(new_processed_data)

    data_dict = dict(PCA1=model_array[:, 0], PCA2=model_array[:, 1]) #####
    model_results = pd.DataFrame(data_dict)
    print(model_results)

    fig = model_results.plot.scatter(x= "PCA1", y= "PCA2", c= 'DarkBlue')
    fig.show()
    

    print("finish")