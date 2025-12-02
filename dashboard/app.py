import streamlit as st
from styles import load_css

st.set_page_config(
    page_title="ML Analytics Dashboard",
    page_icon="🔥",
    layout="wide"
)

# Inject custom CSS
st.markdown(load_css(), unsafe_allow_html=True)

# Header
st.markdown("<h1 class='gradient-text'>🔥 ML Analytics Dashboard</h1>", unsafe_allow_html=True)

st.write("Use the sidebar to navigate between pages.")
