# ---- FIX PATH FIRST ----
import os, sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from fix_path import *   # ensures .env + root importable
# -------------------------
from sb_client.db_client import fetch_table
import pandas as pd
import numpy as np

OUTPUT_CSV = "data/cleaned_data.csv"


def extract():
    print("📌 Extracting raw_data from Supabase...")
    df = pd.DataFrame(fetch_table("raw_data"))
    print("Rows fetched:", len(df))
    return df


def transform(df):
    print("🔧 Transforming...")

    df = df.drop(columns=["id"], errors="ignore")

    # cleanup
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].astype(str).str.strip()

    df["totalcharges"] = pd.to_numeric(df["totalcharges"], errors="coerce")
    df["monthlycharges"] = pd.to_numeric(df["monthlycharges"], errors="coerce")

    df = df.dropna(subset=["totalcharges", "monthlycharges"])

    yes_no_cols = [
        "partner", "dependents", "phoneservice", "multiplelines",
        "onlinesecurity", "onlinebackup", "deviceprotection",
        "techsupport", "streamingtv", "streamingmovies",
        "paperlessbilling", "churn"
    ]

    for col in yes_no_cols:
        df[col] = df[col].map({"Yes": 1, "No": 0}).fillna(0).astype(int)

    df["seniorcitizen"] = df["seniorcitizen"].astype(int)

    ohe_cols = ["gender", "internetservice", "contract", "paymentmethod"]
    df = pd.get_dummies(df, columns=ohe_cols, drop_first=True)

    df.columns = (
        df.columns.str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.where(pd.notnull(df), None)

    print("Final shape:", df.shape)
    return df


def load(df):
    print("📁 Saving to cleaned_data.csv...")
    df.to_csv(OUTPUT_CSV, index=False)
    print("✅ Saved:", OUTPUT_CSV)


def run():
    print("\n====== ETL START ======\n")
    df = extract()
    clean = transform(df)
    load(clean)
    print("\n====== ETL DONE ======\n")


if __name__ == "__main__":
    run()
