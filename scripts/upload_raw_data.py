import pandas as pd
from sb_client import create_client
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# Load CSV
df = pd.read_csv(r"C:/Users/ppriy/Downloads/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Normalize column names
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Strip whitespace from ALL string columns
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Replace empty strings with None
df = df.replace({"": None, " ": None})

# Convert numeric columns
df["totalcharges"] = pd.to_numeric(df["totalcharges"], errors="coerce")
df["monthlycharges"] = pd.to_numeric(df["monthlycharges"], errors="coerce")

# FINAL FIX: Replace ANY remaining NaN with None
df = df.replace({np.nan: None})

print("Checking for NaN values now...")
print(df.isna().sum())

# Convert to list of dicts
records = df.to_dict(orient="records")

batch_size = 500
for i in range(0, len(records), batch_size):
    batch = records[i:i+batch_size]
    response = supabase.table("raw_data").insert(batch).execute()
    print(response)

print("UPLOAD COMPLETE")
