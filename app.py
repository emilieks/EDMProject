import streamlit as st

st.write("# Valenbisi Statistics and Predictions")

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_Predict_Free_Parking.py", 
                 label="Predict Free Parking")

with col2:
    st.page_link("pages/2_test2.py", 
                 label="Test 2")

