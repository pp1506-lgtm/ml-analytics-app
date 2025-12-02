import fix_path
import streamlit as st
import pandas as pd
import requests
from styles import load_css
import os, sys

# Fix import path so API works
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT not in sys.path:
    sys.path.append(ROOT)

API_URL = "http://127.0.0.1:8000/predict/batch"

# Header
st.markdown(load_css(), unsafe_allow_html=True)
st.markdown("<h2 class='gradient-text'>📦 Batch Churn Prediction</h2>", unsafe_allow_html=True)

uploaded = st.file_uploader("Upload a CSV file of customers", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    st.write("### 👀 Preview of Uploaded Data")
    st.dataframe(df.head(5), use_container_width=True)

    if st.button("🚀 Run Batch Prediction"):
        with st.spinner("Predicting churn for all rows..."):
            response = requests.post(API_URL, json=df.to_dict(orient="records"))
            preds = response.json()["predictions"]

        df["Churn_Probability"] = preds
        st.success("🎉 Prediction complete!")

        st.write("### 📊 Results")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇ Download Results CSV",
            csv,
            "batch_predictions.csv",
            "text/csv"
        )
else:
    st.info("Upload a CSV file to begin.")
