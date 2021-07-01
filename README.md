# Autonomic nervous system reactivity during VR stimulation
## for Dr. Meir Plotnik's lab

**Created as part of the hackathon final project in the course "Python for neurosceintists" - Sagol School of Neuroscience, Tel-Aviv University.**

**By: Liraz Attia, Benny Kupchinetsky, Keren Ruzal, Taly Ohad**

This package allows reaserchers to process GSR, ECG, and respiration raw data, to calculate "stress score" and visualize it.
We offer tools for visualizing the "stress score" changes over time, either offline or online during data aquisition.
In addition, this package allows to process speech data, and show correlational data to the other metrics.


# Contents
This resipetory includes few files that you'll need to have before you start analysing:
1. **Processing.py** - This file is the main file which defines the parent class "OfflineAnalysisANS", and all it's methods for the raw-data processing, stress-score makeing, and visualizing.
2. **visualization_bar.py** - This file containes child classes and methods allowing to process and visualize the stress-score online, during an experiment.
3. **test_offline.py** - In here you can find few tests for all the methods.
4. **Data.csv** - An example of real raw data that serves as an input for the parent class. It contains 4 columns: TIME, ECG, GSR, and RESP.

# Usage
Below is an example of the minimal usage flow requiered for recieving a result:
![image](https://user-images.githubusercontent.com/80268425/124131136-2a98da80-da88-11eb-955e-5ae613510586.png)
![Figure_1](https://user-images.githubusercontent.com/80268425/124130351-5798bd80-da87-11eb-9acb-3b74b36ad556.png)
