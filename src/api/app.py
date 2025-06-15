import os
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
import uvicorn

from .config import settings
from .services.model_service import model_service

class WineFeatures(BaseModel):
    fixed_acidity: float = Field(..., ge=0, le=20, description="Fixed acidity (tartaric acid - g/dm³)")
    volatile_acidity: float = Field(..., ge=0, le=2, description="Volatile acidity (acetic acid - g/dm³)")
    citric_acid: float = Field(..., ge=0, le=1, description="Citric acid (g/dm³)")
    residual_sugar: float = Field(..., ge=0, le=20, description="Residual sugar (g/dm³)")
    chlorides: float = Field(..., ge=0, le=1, description="Chlorides (sodium chloride - g/dm³)")
    free_sulfur_dioxide: float = Field(..., ge=0, le=100, description="Free sulfur dioxide (mg/dm³)")
    total_sulfur_dioxide: float = Field(..., ge=0, le=300, description="Total sulfur dioxide (mg/dm³)")
    density: float = Field(..., ge=0.9, le=1.1, description="Density (g/cm³)")
    pH: float = Field(..., ge=2, le=5, description="pH")
    sulphates: float = Field(..., ge=0, le=2, description="Sulphates (potassium sulphate - g/dm³)")
    alcohol: float = Field(..., ge=8, le=15, description="Alcohol (% by volume)")

    @field_validator('*', mode='before')
    @classmethod
    def validate_numeric(cls, v):
        if pd.isna(v) or v is None:
            raise ValueError("All features must be provided and cannot be null")
        return float(v)

class PredictionRequest(BaseModel):
    features: WineFeatures
    model_version: Optional[str] = Field(None, description="Specific model version to use (optional)")

class PredictionResponse(BaseModel):
    prediction: float = Field(..., description="Predicted wine quality score")
    model_used: str = Field(..., description="Model type used for prediction")
    model_version: str = Field(..., description="Version of the model used")
    prediction_timestamp: str = Field(..., description="Timestamp of prediction")
    confidence_interval: Optional[Dict[str, float]] = Field(None, description="Confidence interval if available")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Service health status")
    timestamp: str = Field(..., description="Current timestamp")
    model_loaded: bool = Field(..., description="Whether model is loaded successfully")
    model_info: Dict[str, Any] = Field(..., description="Information about loaded model")

class ModelInfoResponse(BaseModel):
    model_type: str = Field(..., description="Type of the model")
    model_version: str = Field(..., description="Version of the model")
    training_date: str = Field(..., description="When the model was trained")
    metrics: Dict[str, float] = Field(..., description="Model performance metrics")
    features: List[str] = Field(..., description="List of required features")
    model_path: str = Field(..., description="Path to the model file")

def get_healthcheck() -> HealthResponse:
    try:
        model_loaded = model_service.is_model_loaded()
        model_info = model_service.get_model_info() if model_loaded else {}
        
        return HealthResponse(
            status="healthy" if model_loaded else "unhealthy",
            timestamp=datetime.now().isoformat(),
            model_loaded=model_loaded,
            model_info=model_info
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.now().isoformat(),
            model_loaded=False,
            model_info={"error": str(e)}
        )

def get_model_info_service():
    try:
        model_info = model_service.get_model_info()
        
        feature_names = [
            "fixed_acidity", "volatile_acidity", "citric_acid", "residual_sugar",
            "chlorides", "free_sulfur_dioxide", "total_sulfur_dioxide", 
            "density", "pH", "sulphates", "alcohol"
        ]
        
        return ModelInfoResponse(
            model_type=model_info['model_type'],
            model_version=model_info['model_version'],
            training_date=model_info['training_date'],
            metrics=model_info['metrics'],
            features=feature_names,
            model_path=model_info['model_path']
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get model info: {str(e)}"
        )

def make_prediction(request: PredictionRequest):
    try:
        features_dict = request.features.model_dump()
        features_df = pd.DataFrame([features_dict])
        
        prediction = model_service.predict(features_df)
        model_info = model_service.get_model_info()
        
        return PredictionResponse(
            prediction=prediction,
            model_used=model_info['model_type'],
            model_version=model_info['model_version'],
            prediction_timestamp=datetime.now().isoformat(),
            confidence_interval=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        model_service.load_best_model()
        print("Model loaded successfully on startup")
    except Exception as e:
        print(f"Failed to load model on startup: {e}")
    
    yield
    
    print("Application shutting down...")

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

@app.get("/healthcheck", response_model=HealthResponse)
async def healthcheck():
    return get_healthcheck()

@app.get("/model-info", response_model=ModelInfoResponse)
async def get_model_info():
    return get_model_info_service()

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    return make_prediction(request)

@app.get("/")
async def root():
    return {
        "message": settings.app_name,
        "version": settings.app_version,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "endpoints": {
            "predict": "/predict",
            "healthcheck": "/healthcheck", 
            "model_info": "/model-info",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level
    ) 