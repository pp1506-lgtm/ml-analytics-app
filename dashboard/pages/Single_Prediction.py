import fix_path
import streamlit as st
import pandas as pd
import requests
from styles import load_css

st.markdown(load_css(), unsafe_allow_html=True)
st.markdown("<h2 class='gradient-text'>🎯 Single Customer Prediction</h2>", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000/predict/churn"

# Input fields
col1, col2, col3 = st.columns(3)

with col1:
    seniorcitizen = st.number_input("Senior Citizen (0/1)", 0, 1)
    partner = st.number_input("Partner (0/1)", 0, 1)
    dependents = st.number_input("Dependents (0/1)", 0, 1)

with col2:
    tenure = st.number_input("Tenure (months)", 0)
    phoneservice = st.number_input("Phone Service (0/1)", 0, 1)
    multiplelines = st.number_input("Multiple Lines (0/1)", 0, 1)

with col3:
    monthlycharges = st.number_input("Monthly Charges", 0.0)
    totalcharges = st.number_input("Total Charges", 0.0)

# Hidden encoded columns default to 0
encoded_cols = [
    "onlinesecurity", "onlinebackup", "deviceprotection",
    "techsupport", "streamingtv", "streamingmovies",
    "paperlessbilling", "gender_male",
    "internetservice_fiber_optic", "internetservice_no",
    "contract_one_year", "contract_two_year",
    "paymentmethod_credit_card_automatic",
    "paymentmethod_electronic_check",
    "paymentmethod_mailed_check"
]

if st.button("Predict"):
    payload = {
        "seniorcitizen": seniorcitizen,
        "partner": partner,
        "dependents": dependents,
        "tenure": tenure,
        "phoneservice": phoneservice,
        "multiplelines": multiplelines,
        "monthlycharges": monthlycharges,
        "totalcharges": totalcharges,
    }

    # add encoded columns as zero
    for col in encoded_cols:
        payload[col] = 0

    response = requests.post(API_URL, json=payload)
    prob = response.json()["churn_probability"]

    st.success(f"🔥 Churn Probability: **{prob:.2f}**")
    if prob >= 0.5:
        st.warning("⚠️ This customer is likely to churn.")
    else:
        st.info("✅ This customer is unlikely to churn.")