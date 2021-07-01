# Autonomic nervous system reactivity during VR stimulation
## for Dr. Meir Plotnik's lab

**Created as part of the hackathon final project in the course "Python for neuroscientists" - Sagol School of Neuroscience, Tel-Aviv University.**

**By: Liraz Attia, Benny Kupchinetsky, Keren Ruzal, Taly Ohad**

This package allows researchers to process GSR, ECG, and respiration raw data, to calculate "stress score" and visualize it.
We offer tools for visualizing the "stress score" changes over time, either offline or online during data acquisition.
In addition, this package allows to process speech data, and shows correlational data to the other metrics.


# Contents
This repository includes a few files that you'll need to have before you start analyzing:
1. **offline_processing.py** - This file is the main file that defines the parent class "OfflineAnalysisANS", and all its methods for raw-data processing, stress-score making, and visualizing.
2. **online_processing.py.py** - This file is the file that defines the child class "OnlineAnalysisANS" (inherits from "OfflineAnalysisANS"), and all its methods for raw-data processing and stress-score making.
3. **online_simulation.py** - This file contains child classes and methods allowing to simulate processing and visualizing the stress-score online, during an experiment.
4. **test_offline.py** - In here you can find few tests for all the methods of the offline processing.
5. **wav_anlz.py** - few functions that allow finding initial correlation of speech data to the other processed data.
6. **Data.csv** - An example of real raw data that serves as an input for the parent class. It contains 4 columns: TIME, ECG, GSR, and RESP. The auditory data are not included due to their heaviness.

# Usage
Below is an example of the minimal usage flow required for receiving a result:
![image](https://user-images.githubusercontent.com/80268425/124131773-cb879580-da88-11eb-9237-afbf24428b61.png)
Offline processing and plotting of the data:
![Figure_1](https://user-images.githubusercontent.com/80268425/124130351-5798bd80-da87-11eb-9acb-3b74b36ad556.png)
Online processing and plotting of the data:
![Figure_2](src\ANS_reactivity\graph.JPG)
![Figure_3](src\ANS_reactivity\plot.JPG)

