from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ADD THIS LINE
from api.schemas import ChurnRequest, BatchChurnRequest
from api.predict_churn import predict_single, predict_batch

app = FastAPI(
    title="Churn Prediction API",
    version="1.0.0",
    description="ML-powered churn prediction service"
)

# ADD THIS ENTIRE BLOCK - Put it right after creating the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins including Framer
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
def predict_batch_api(payload: BatchChurnRequest):
    return predict_batch([record.dict() for record in payload.records])