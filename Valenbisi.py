import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.write("# Valenbisi")

st.write("Welcome to Valenbisi bike stand prediction! Plan your next trip with valenbisi here!")
st.write("What would you like to do?")

st.markdown('<a href="#data_visualization" target="_self"><b>View valenbisi data</b></a>', unsafe_allow_html=True)
st.markdown('<a href="Plan_Your_Valenbisi_Trip" target="_self"><b>Plan a valenbisi trip ahead of time</b></a>', unsafe_allow_html=True)
st.markdown('<a href="Predict_Free_Parking_Space" target="_self"><b>Check if there is available parking spots at destination</b></a>', unsafe_allow_html=True)

@st.cache_data
def load_new():
    # ideally this would continuously come from source
    return pd.read_csv('streamlitdata/NewestData.csv')

@st.cache_data
def load_station_info():
    return pd.read_csv("streamlitdata/STATIONS.csv")

@st.cache_data
def get_count_map(df, target):

    # Create folium map centered around Valencia
    traffic_map = folium.Map(location=[39.4701, -0.3704], zoom_start=13)

    for _, row in df.iterrows():
        location = (row['Latitude'], row['Longitude'])
        
        # Circle
        folium.CircleMarker(
            location=location,
            popup=row['Direction'],
            radius=9,
            color='white',
            fill=True,
            fill_opacity=0.9
        ).add_to(traffic_map)
        
        # Number label
        label = folium.Marker(
            location=location,
            popup=row['Direction'],
            icon=folium.DivIcon(
                icon_size=(140,26),
                icon_anchor=(4, 8),
                html=f'<div style="font-size:10pt; color:black;"><b>  {row[target]}</b></div>'
            )
        )
        traffic_map.add_child(label)

    return traffic_map

st.markdown('<a id="data_visualization"></a>', unsafe_allow_html=True)

st.write("## Current bike count at stations")
new_data = load_new()
date_string = new_data.iloc[0]['Update_date']
date_datetime = pd.to_datetime(date_string)

pretty_date = date_datetime.strftime("%B %d, %Y, %I:%M %p")
selection = st.radio("", ["Free Bikes", "Free Stands"])
st.write(f"Number of {selection} at last update, {pretty_date}")
target = 'Free_bici' if selection=='Free Bikes' else 'Free_stand'
count_map = get_count_map(new_data, target)
map_result = st_folium(count_map, width=700, height=500)

# See station information
station_info = load_station_info()
st.markdown(" ", unsafe_allow_html=True) 
st.write("### Click on a station to see information:")
if map_result and map_result.get("last_object_clicked_popup"):
    clicked_direction = map_result["last_object_clicked_popup"]
empty_df = pd.DataFrame(columns=station_info.columns)
st.write(station_info[station_info['Direction'] == clicked_direction] if 'clicked_direction' in locals() else empty_df)