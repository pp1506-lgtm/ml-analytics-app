import fix_path
import streamlit as st
import pandas as pd
from sklearn.decomposition import PCA
import plotly.express as px
from styles import load_css

st.markdown(load_css(), unsafe_allow_html=True)
st.markdown("<h2 class='gradient-text'>🔮 Customer Segmentation (PCA)</h2>", unsafe_allow_html=True)

df = pd.read_csv("data/cleaned_data.csv")

features = df.drop(columns=["customerid", "churn"])

pca = PCA(n_components=2)
components = pca.fit_transform(features)

df["PC1"] = components[:, 0]
df["PC2"] = components[:, 1]

fig = px.scatter(
    df,
    x="PC1",
    y="PC2",
    color=df["churn"].map({0: "Not Churned", 1: "Churned"}),
    color_discrete_map={
        "Not Churned": "#4ade80",
        "Churned": "#f87171"
    },
    title="Customer Segmentation (PCA Projection)"
)

st.plotly_chart(fig, use_container_width=True)
