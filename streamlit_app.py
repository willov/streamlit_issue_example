import os
import json
import pandas as pd
import numpy as np
import streamlit as st
import sys

import subprocess
import sys

if "sund" not in os.listdir('./custom_package'):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--target=./custom_package", 'https://isbgroup.eu/edu/assets/sund-1.0.1.tar.gz#sha256=669a1d05c5c8b68500086e183d831650277012b3ea57e94356de1987b6e94e3e'])

sys.path.append('./custom_package')
import sund

# Setup the model and simulation

model_name = 'test_model'
sund.installModel(f"{model_name}.txt")
model_class = sund.importModel(model_name)
model = model_class() 

features = model.featurenames

sim = sund.Simulation(models = [model], timeunit='s')
# Start the app

st.title("Simulation permission error example")
st.markdown(""" The models are simulating using the custom package `sund`, which compiles the model defined in the text file `test_model.txt`. On the Streamlit Cloud, this results in a permission error, but it works fine locally. 
            
The packages needed are listed in the `requirements.txt` file, installed with pip. 

This simple application should be able to select the simulation length, and plot one of the available features. 
             
""")

end_time = st.slider("Simulation length:", 1.0, 20.0, 5.0)

sim.Simulate(timevector = np.linspace(0.0,end_time,500), resetstatesderivatives=True)
sim_results = pd.DataFrame(sim.featuredata,columns=sim.featurenames)
sim_results.insert(0, 'Time', sim.timevector)

st.subheader("Plotting the time course given the alcoholic drinks specified")
feature = st.selectbox("Feature of the model to plot", features, index=1)
st.line_chart(sim_results, x="Time", y=feature)
