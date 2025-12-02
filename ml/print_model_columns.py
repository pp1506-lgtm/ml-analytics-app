import joblib

model = joblib.load(r"C:\Users\ppriy\ml-analytics-app\ml\models\churn_model.pkl")
print("\n=== MODEL FEATURE NAMES ===\n")
print(list(model.feature_names_in_))
