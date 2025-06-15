import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import joblib

st.title("Free Parking Stands At End Station")
st.write("Are you currently traveling with valenbisi and want to check if there is available parking spots?")
st.write("Use our machine learning model to predict available parking stands!")

@st.cache_data
def load_model():
    return joblib.load("rf_model.pkl")

@st.cache_data
def load_station_info():
    return pd.read_csv("streamlitdata/STATIONS.csv")

@st.cache_data
def load_new():
    # ideally this would continuously come from source
    return pd.read_csv('streamlitdata/NewestData.csv')

@st.cache_data
def load_3new():
    return pd.read_csv('streamlitdata/3NewestData.csv')

@st.cache_data
def get_station_map(station_data):
    m = folium.Map(
        location=[station_data['Latitude'].mean(), station_data['Longitude'].mean()+0.01],
        zoom_start=13
    )
    for _, row in station_data.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=row['Direction'],  # This string will be returned if clicked
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
    return m

st.write("## Predict Free stands at your end station")

# Get station info and current date(from main page)
station_info = load_station_info()
stations = station_info['Direction'].unique()

new_data = load_new()
date_string = new_data.iloc[0]['Update_date']
date_datetime = pd.to_datetime(date_string)
current_datetime = pd.to_datetime(date_string)

# Select station
st.write("#### Select end station:")

selected_station = st.selectbox("", stations, 0)
st.session_state['selected_station'] = selected_station

st.write("")
st.write("")
# Select on map
def get_station_map(station_data):
    m = folium.Map(
        location=[station_data['Latitude'].mean(), station_data['Longitude'].mean() + 0.01],
        zoom_start=13
    )
    for _, row in station_data.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=row['Direction'],  # This string will be returned if clicked
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
    return m
# Add a button to toggle map visibility
if 'show_map' not in st.session_state:
    st.session_state['show_map'] = False  # Default state: hide the map
if st.button("Choose on Map"):
    st.session_state['show_map'] = not st.session_state['show_map']

# Expander to show the map 
if st.session_state['show_map']:
    station_map = get_station_map(station_info)
    map_result = st_folium(station_map, width=700, height=500)
    # If the user clicks on the map, capture the station from the popup
    if map_result and map_result.get("last_object_clicked_popup"):
        selected_station = map_result["last_object_clicked_popup"]
        st.session_state['selected_station'] = selected_station

selected_station = st.session_state['selected_station']
st.write(f"Selected station: {selected_station}")

# Get current count
current_free_stands = new_data[new_data['Direction'] == selected_station]['Free_stand'].iloc[0]

# Create input for ml model
# (same as feature_engineering in rf_model)
x = station_info[station_info['Direction'] == selected_station].iloc[0]
x['season'] = pd.to_datetime(current_datetime).month % 12 // 3 + 1
x['is_weekday'] = 1 if pd.to_datetime(current_datetime).weekday() < 5 else 0
x['hour_sin'] = np.sin(2 * np.pi * pd.to_datetime(current_datetime).hour / 24)

time_diff = st.number_input("How many minutes until arrival?", min_value=1, max_value=120, value=15, step=1)

x['Prev_Free_stand'] = current_free_stands
x['time_diff'] = time_diff

# Get earlier data for model, and add to x
new_data_3  = load_3new()
new_data_3['Update_date'] = pd.to_datetime(new_data_3['Update_date'])
new_data_3_station = new_data_3[new_data_3['Direction']==selected_station].sort_values(by='Update_date', ascending=False) # first value, last measure
x['Prev2_Free_stand'] = new_data_3_station['Free_stand'].iloc[1]
x['Prev3_Free_stand'] = new_data_3_station['Free_stand'].iloc[2]

update_dates = new_data_3_station['Update_date'].reset_index(drop=True)
x['time_diff_2'] = (update_dates.iloc[0] - update_dates.iloc[1]).total_seconds() / 60
x['time_diff_3'] = (update_dates.iloc[0] - update_dates.iloc[2]).total_seconds() / 60

# Run model prediction
model = load_model()
feature_names = model.feature_names_in_
model_input = pd.DataFrame([x[feature_names]]) 
prediction = model.predict(model_input)[0]

# round down to closest int
prediction_floor = int(prediction)

col1, col2 = st.columns([3, 1])
with col1:
    st.write(f"### Currently free parking stands:")
    st.write(f"### Predicted free parking stands:")
with col2:
    st.write(f"### {current_free_stands}")
    st.write(f"### {prediction_floor}")