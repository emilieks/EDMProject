import streamlit as st
import pandas as pd
import numpy as np

st.write("# Welcome to test")

st.write("Hello, Streamlit!")

var = st.text_input("Enter some text:")

st.write("You entered:", var)

# Add a slider
x = st.slider("Pick a number", 0, 100, 25)
st.write("You selected:", x)

# Show a chart
df = pd.DataFrame({
    'x': np.arange(10),
    'y': np.random.randn(10)
})
st.line_chart(df)

