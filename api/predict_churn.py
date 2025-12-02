import joblib
import os
import pandas as pd

MODEL_DIR = "ml"

model = joblib.load(os.path.join(MODEL_DIR, "model_random_forest.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
feature_names = joblib.load(os.path.join(MODEL_DIR, "feature_names.pkl"))

NUM_COLS = ["monthlycharges", "totalcharges", "tenure"]

def preprocess(df: pd.DataFrame):
    """Scale numeric columns + ensure correct column order."""
    df = df.copy()
    df[NUM_COLS] = scaler.transform(df[NUM_COLS])
    df = df[feature_names]  # reorder columns exactly as training
    return df

def predict_single(payload: dict):
    df = pd.DataFrame([payload])
    df = preprocess(df)
    pred = model.predict(df)[0]
    proba = model.predict_proba(df)[0][1]
    return {"churn": int(pred), "probability": float(proba)}

def predict_batch(records: list):
    df = pd.DataFrame(records)
    df = preprocess(df)
    preds = model.predict(df)
    probas = model.predict_proba(df)[:, 1]

    results = []
    for p, pr in zip(preds, probas):
        results.append({
            "churn": int(p),
            "probability": float(pr)
        })
    return results
