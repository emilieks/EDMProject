import streamlit as st
import joblib
import pandas as pd
import numpy as np

st.title("Number of Available Parking spots")

@st.cache_data
def load_station_info():
    return pd.read_csv("data/STATIONS.csv")

@st.cache_data
def load_model():
    return joblib.load("model.pkl")

# Get station and information
station_info = load_station_info()
stations = station_info['Direction'].unique()
selected_station = st.selectbox("Select a station", stations)

# Get date
april30 = pd.to_datetime("2023-04-30")
cl1200 = pd.to_datetime("12:00").time()
col1, col2 = st.columns(2)
with col1:
    selected_date = st.date_input("Select a date:", april30)
with col2:
    selected_time = st.time_input("Select a time:", cl1200)
selected_datetime = pd.to_datetime(f"{selected_date} {selected_time}")

# Create input for ml model
x = station_info[station_info['Direction'] == selected_station].iloc[0]
x['season'] = pd.to_datetime(selected_datetime).month % 12 // 3 + 1
x['is_weekday'] = 1 if pd.to_datetime(selected_datetime).weekday() < 5 else 0
x['hour_sin'] = np.sin(2 * np.pi * pd.to_datetime(selected_datetime).hour / 24)

# Run model prediction
model, feature_names = load_model()
model_input = x[feature_names].values.reshape(1, -1)
prediction = model.predict(model_input)

st.write("Selected station information:")
st.write(station_info[station_info['Direction'] == selected_station].iloc[0])


st.write("Prediction for the selected station:")
st.write(prediction[0])

