import sund
import os
import json
import pandas as pd
import numpy as np
import streamlit_app as st

st.elements.utils._shown_default_value_warning=True # This is not a good solution, but it hides the warning of using default values and sessionstate api

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
