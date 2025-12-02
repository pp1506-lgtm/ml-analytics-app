import fix_path
import streamlit as st
import pandas as pd
from styles import load_css

# Header style
st.markdown(load_css(), unsafe_allow_html=True)
st.markdown("<h2 class='gradient-text'>📊 Dataset Overview</h2>", unsafe_allow_html=True)

df = pd.read_csv("data/cleaned_data.csv")

st.write("### 🔍 First 10 Records")
st.dataframe(df.head(10), use_container_width=True)

st.write("### 📉 Summary Statistics")
st.dataframe(df.describe(), use_container_width=True)

st.write("### 🧮 Column Information")
st.write(df.dtypes)
