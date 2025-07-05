import os
print("Running from:", os.getcwd())

#import all necessary libraries
import pandas as pd
import numpy as np
import joblib
import pickle
import streamlit as st

#load the modeland structure
model = joblib.load("pollution_model.pkl")
model_cols = joblib.load(r"C:\Users\HP\OneDrive\Desktop\project\model_colums.pkl")

#lets create an user interface
st.title("water pollutants predictor")
st.write("predict the water pollutants based on Year and Station ID")

#user inputs
year_input = st.number_input("Enter Year", min_value=2000, max_value=2100, value=2022)
station_id = st.text_input("Enter station ID", value='1')

#to encode and then predict
if st.button('Predict'):
    if not station_id:
        st.warning('Please enter the Station ID')
    else:
        #prepare the input
        input_df = pd.DataFrame({'year': [year_input], 'id':[station_id]})
        input_encoded = pd.get_dummies(input_df, columns=['id'])

        #align with model cols
        for col in model_cols:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[model_cols]

        #predict
        predicted_pollutants = model.predict(input_encoded) [0]
        pollutants = ['NH4','BSK5','Suspended','O2','NO3','NO2','SO4','PO4','CL']

        st.subheader(f"Predicted pollutant levels for the station '{station_id}' in {year_input}:")
        predicted_values = {}
        for p, val in zip(pollutants, predicted_pollutants):
            st.write(f'{p}:{val:.2f}')
