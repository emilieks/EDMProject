import streamlit as st
import pandas as pd

st.title("Available Bikes and Stands")
st.write("Are you travelling using valenbisi in the future?")
st.write("Use data to check if you can expect a free bike at your starting station, and a free parking at your end station!")


@st.cache_data
def load_station_info():
    return pd.read_csv("streamlitdata/STATIONS.csv")

@st.cache_data
def load_hourly_data():
    return pd.read_csv("streamlitdata/HourlyCount.csv")

@st.cache_data
def load_weekly_data():
    return pd.read_csv("streamlitdata/WeekdayAverages.csv")

# Load data
station_info = load_station_info()
hourly_count = load_hourly_data()
weekly_count = load_weekly_data()
stations = station_info['Direction'].unique()

# Get station and information
st.write("## Select start and end station:")
col1, col2 = st.columns(2)

with col1:
    selected_station = st.selectbox("Start station", stations, 0)
    selected_station_number = station_info[station_info['Direction'] == selected_station]['Number'].values[0]
with col2:
    selected_endstation = st.selectbox("End station", stations, 1)
    selected_endstation_number = station_info[station_info['Direction'] == selected_endstation]['Number'].values[0]

st.write("## Average count for each hour of the day:")
st.write("Here you can see if it normally is available bikes and stands at your travel time.")

# Choose weekday if wanted
choices = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
selected_day = st.radio("Filter on day:", choices, horizontal=True)

# get correct count
if selected_day == 'All':
    station_hourly_count = hourly_count[hourly_count['StationNumber'] == selected_station_number]
    endstation_hourly_count = hourly_count[hourly_count['StationNumber'] == selected_endstation_number]

else:
    station_hourly_count = weekly_count[(weekly_count['StationNumber'] == selected_station_number) & (weekly_count['Weekday']==selected_day)]
    endstation_hourly_count = weekly_count[(weekly_count['StationNumber'] == selected_endstation_number) & (weekly_count['Weekday']==selected_day)]

col1, col2 = st.columns(2)
with col1:
    st.write("##### Number of Free Bikes")
    st.line_chart(station_hourly_count.set_index('HourOfDay')['Avg_Free_Bici'], use_container_width=True, x_label="hour of day", )
with col2:
    st.write("##### Number of Free Stands")
    st.line_chart(endstation_hourly_count.set_index('HourOfDay')['Avg_Free_Stand'], use_container_width=True, x_label="hour of day")

