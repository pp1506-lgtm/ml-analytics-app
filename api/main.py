
from fastapi import FastAPI
from api.schemas import ChurnRequest, BatchChurnRequest
from api.predict_churn import predict_single, predict_batch

app = FastAPI(
    title="Churn Prediction API",
    version="1.0.0",
    description="ML-powered churn prediction service"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict/churn")
def predict_churn(payload: ChurnRequest):
    return predict_single(payload.dict())

@app.post("/predict/batch")
def predict_batch_api(payload: BatchChurnRequest):
    return predict_batch([record.dict() for record in payload.records])
