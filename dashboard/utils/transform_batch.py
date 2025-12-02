import pandas as pd
import numpy as np

MODEL_COLUMNS = [
    'seniorcitizen', 'partner', 'dependents', 'tenure',
    'phoneservice', 'multiplelines', 'onlinesecurity', 'onlinebackup',
    'deviceprotection', 'techsupport', 'streamingtv', 'streamingmovies',
    'paperlessbilling', 'monthlycharges', 'totalcharges',
    'gender_male', 'internetservice_fiber_optic', 'internetservice_no',
    'contract_one_year', 'contract_two_year',
    'paymentmethod_credit_card_automatic', 'paymentmethod_electronic_check',
    'paymentmethod_mailed_check'
]

YES_NO_COLS = [
    "partner", "dependents", "phoneservice", "multiplelines",
    "onlinesecurity", "onlinebackup", "deviceprotection",
    "techsupport", "streamingtv", "streamingmovies",
    "paperlessbilling"
]


def clean_batch_df(df: pd.DataFrame) -> pd.DataFrame:
    """Transform raw Telco CSV into EXACT model input."""
    
    # --- Normalize column names ---
    df.columns = (
        df.columns.str.lower()
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )

    # --- Strip whitespace ---
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

    # --- Numeric fields ---
    for col in ["monthlycharges", "totalcharges", "tenure"]:
        df[col] = pd.to_numeric(df.get(col, 0), errors="coerce").fillna(0)

    df["seniorcitizen"] = pd.to_numeric(df.get("seniorcitizen", 0), errors="coerce").fillna(0).astype(int)

    # --- Yes/No conversion ---
    yes_no_map = {"yes": 1, "no": 0, "Yes": 1, "No": 0}
    for col in YES_NO_COLS:
        if col in df.columns:
            df[col] = df[col].map(yes_no_map).fillna(0).astype(int)
        else:
            df[col] = 0

    # --- One-hot encode raw text columns ---
    ohe_cols = ["gender", "internetservice", "contract", "paymentmethod"]
    for c in ohe_cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.lower().str.strip()

    df = pd.get_dummies(df, columns=ohe_cols, drop_first=True)

    # --- Normalize the newly created OHE names ---
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace("-", "_")

    # --- Create missing OHE columns (model expects these) ---
    forced_ohe_map = {
        'gender_male': 'gender_male',
        'internetservice_fiber_optic': 'internetservice_fiber_optic',
        'internetservice_no': 'internetservice_no',
        'contract_one_year': 'contract_one_year',
        'contract_two_year': 'contract_two_year',
        'paymentmethod_credit_card_automatic': 'paymentmethod_credit_card_(automatic)',
        'paymentmethod_electronic_check': 'paymentmethod_electronic_check',
        'paymentmethod_mailed_check': 'paymentmethod_mailed_check',
    }

    # Ensure every required column exists
    for clean_col, raw_col in forced_ohe_map.items():
        matches = [c for c in df.columns if raw_col in c]
        if matches:
            df[clean_col] = df[matches[0]]
        else:
            df[clean_col] = 0

    # --- Final ordering ---
    df = df.reindex(columns=MODEL_COLUMNS, fill_value=0)

    return df
