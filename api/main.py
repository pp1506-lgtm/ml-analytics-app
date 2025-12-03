from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import ChurnRequest, BatchChurnRequest
from api.predict_churn import predict_single, predict_batch
import pandas as pd
import io

app = FastAPI(
    title="Churn Prediction API",
    version="1.0.0",
    description="ML-powered churn prediction service"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict/churn")
def predict_churn(payload: ChurnRequest):
    return predict_single(payload.dict())

@app.post("/predict/batch")
async def predict_batch_api(file: UploadFile = File(...)):
    """
    Accept CSV file upload (raw Telco format OR preprocessed format)
    Returns batch predictions
    """
    try:
        # Read the CSV file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Check if CSV is already in model format (has seniorcitizen column)
        # or needs transformation (has SeniorCitizen column)
        if 'SeniorCitizen' in df.columns:
            # Transform raw Telco CSV to model format
            df = transform_telco_to_model_format(df)
        
        # Convert DataFrame to list of dicts
        records = df.to_dict('records')
        
        # Call your prediction function
        result = predict_batch(records)
        
        return result
        
    except Exception as e:
        return {"error": str(e), "message": "Make sure CSV has the correct columns"}


def transform_telco_to_model_format(df):
    """
    Transform raw Telco Customer Churn CSV to model input format
    """
    transformed = pd.DataFrame()
    
    # Direct mappings (binary)
    transformed['seniorcitizen'] = df['SeniorCitizen'].fillna(0).astype(int)
    transformed['partner'] = (df['Partner'] == 'Yes').astype(int)
    transformed['dependents'] = (df['Dependents'] == 'Yes').astype(int)
    
    # Numeric fields
    transformed['tenure'] = df['tenure'].fillna(0).astype(int)
    transformed['monthlycharges'] = df['MonthlyCharges'].fillna(0).astype(float)
    
    # Handle TotalCharges (sometimes has spaces/non-numeric values)
    transformed['totalcharges'] = pd.to_numeric(
        df['TotalCharges'].replace(' ', '0'), 
        errors='coerce'
    ).fillna(0).astype(float)
    
    # Services (binary)
    transformed['phoneservice'] = (df['PhoneService'] == 'Yes').astype(int)
    transformed['multiplelines'] = (df['MultipleLines'] == 'Yes').astype(int)
    transformed['onlinesecurity'] = (df['OnlineSecurity'] == 'Yes').astype(int)
    transformed['onlinebackup'] = (df['OnlineBackup'] == 'Yes').astype(int)
    transformed['deviceprotection'] = (df['DeviceProtection'] == 'Yes').astype(int)
    transformed['techsupport'] = (df['TechSupport'] == 'Yes').astype(int)
    transformed['streamingtv'] = (df['StreamingTV'] == 'Yes').astype(int)
    transformed['streamingmovies'] = (df['StreamingMovies'] == 'Yes').astype(int)
    transformed['paperlessbilling'] = (df['PaperlessBilling'] == 'Yes').astype(int)
    
    # Gender (one-hot)
    transformed['gender_male'] = (df['gender'] == 'Male').astype(int)
    
    # Internet Service (one-hot)
    transformed['internetservice_fiber_optic'] = (df['InternetService'] == 'Fiber optic').astype(int)
    transformed['internetservice_no'] = (df['InternetService'] == 'No').astype(int)
    
    # Contract (one-hot)
    transformed['contract_one_year'] = (df['Contract'] == 'One year').astype(int)
    transformed['contract_two_year'] = (df['Contract'] == 'Two year').astype(int)
    
    # Payment Method (one-hot)
    transformed['paymentmethod_credit_card_automatic'] = (
        df['PaymentMethod'] == 'Credit card (automatic)'
    ).astype(int)
    transformed['paymentmethod_electronic_check'] = (
        df['PaymentMethod'] == 'Electronic check'
    ).astype(int)
    transformed['paymentmethod_mailed_check'] = (
        df['PaymentMethod'] == 'Mailed check'
    ).astype(int)
    
    return transformed