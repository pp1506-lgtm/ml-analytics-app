(check master branch)

ML-Powered Churn Prediction API (FastAPI)

This repository contains the FastAPI backend for a machine learning based **Customer Churn Prediction Service**.  
It exposes production-ready API endpoints for **single customer prediction** and **batch CSV processing**.

Features

- FastAPI backend with fully documented Swagger UI
- Machine Learning model for churn prediction
- Single prediction API (`POST /predict/churn`)
- Batch prediction API (`POST /predict/batch`)
- Deployed on Render
- Automatic CORS handling for frontend integration
- Pydantic request validation
- CSV → DataFrame → Model pipeline
- API Endpoints
- Health Check
