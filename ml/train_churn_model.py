import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

DATA_PATH = "data/cleaned_data.csv"
MODEL_DIR = "ml"

FEATURE_COLS = [
    'seniorcitizen', 'partner', 'dependents', 'tenure', 'phoneservice',
    'multiplelines', 'onlinesecurity', 'onlinebackup', 'deviceprotection',
    'techsupport', 'streamingtv', 'streamingmovies', 'paperlessbilling',
    'monthlycharges', 'totalcharges',
    'gender_male', 'internetservice_fiber_optic', 'internetservice_no',
    'contract_one_year', 'contract_two_year',
    'paymentmethod_credit_card_automatic',
    'paymentmethod_electronic_check',
    'paymentmethod_mailed_check'
]

TARGET_COL = "churn"


def load_data():
    print("📌 Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    print("✔ Loaded:", df.shape)
    return df


def train_model(df):
    print("📌 Preparing data...")

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Standardize numerical features
    num_cols = ["monthlycharges", "totalcharges", "tenure"]
    scaler = StandardScaler()
    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test[num_cols] = scaler.transform(X_test[num_cols])

    # Random Forest
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        class_weight="balanced",
        random_state=42
    )

    print("📌 Training model...")
    model.fit(X_train, y_train)
    print("✔ Model trained!")

    # Save everything
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_DIR, "model_random_forest.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))
    joblib.dump(FEATURE_COLS, os.path.join(MODEL_DIR, "feature_names.pkl"))

    print("🎉 Model + Scaler + Features saved in /ml/")


def main():
    df = load_data()
    train_model(df)


if __name__ == "__main__":
    print("======== TRAINING STARTED ========")
    main()
    print("======== TRAINING COMPLETE ========")
