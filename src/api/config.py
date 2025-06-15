import os
from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    app_name: str = "Wine Quality Prediction API"
    app_version: str = "1.0.0"
    app_description: str = "API for predicting wine quality using ML models trained with MLflow and managed by DVC"
    
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    log_level: str = "info"
    
    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_experiment_name: str = "wine_quality_experiment"
    
    model_rf_path: str = "/opt/airflow/project/rf_model.pkl"
    model_lgb_path: str = "/opt/airflow/project/lgb_model.txt"
    
    max_model_cache_size: int = 3
    model_reload_interval: int = 3600
    
    max_request_size: int = 1024
    request_timeout: int = 30


settings = Settings()

def get_environment() -> str:
    return os.getenv("ENVIRONMENT", "development")

def is_development() -> bool:
    return get_environment().lower() == "development"

def is_production() -> bool:
    return get_environment().lower() == "production"

def is_testing() -> bool:
    return get_environment().lower() == "testing" 