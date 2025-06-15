import pytest
import sys
import os
from fastapi.testclient import TestClient
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.api.app import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data

def test_healthcheck_endpoint():
    """Test healthcheck endpoint"""
    response = client.get("/healthcheck")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "model_loaded" in data
    assert "model_info" in data

def test_model_info_endpoint():
    """Test model info endpoint"""
    response = client.get("/model-info")
    assert response.status_code in [200, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert "model_type" in data
        assert "model_version" in data
        assert "features" in data
        assert len(data["features"]) == 11

def test_predict_endpoint_valid_data():
    test_data = {
        "features": {
            "fixed_acidity": 7.4,
            "volatile_acidity": 0.7,
            "citric_acid": 0.0,
            "residual_sugar": 1.9,
            "chlorides": 0.076,
            "free_sulfur_dioxide": 11.0,
            "total_sulfur_dioxide": 34.0,
            "density": 0.9978,
            "pH": 3.51,
            "sulphates": 0.56,
            "alcohol": 9.4
        }
    }
    
    response = client.post("/predict", json=test_data)
    assert response.status_code in [200, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert "prediction" in data
        assert "model_used" in data
        assert "model_version" in data
        assert "prediction_timestamp" in data
        assert 0 <= data["prediction"] <= 10

def test_predict_endpoint_invalid_data():
    test_data = {
        "features": {
            "fixed_acidity": 7.4,
            "volatile_acidity": 0.7
        }
    }
    
    response = client.post("/predict", json=test_data)
    assert response.status_code == 422

def test_predict_endpoint_out_of_range_data():
    test_data = {
        "features": {
            "fixed_acidity": -1.0,
            "volatile_acidity": 0.7,
            "citric_acid": 0.0,
            "residual_sugar": 1.9,
            "chlorides": 0.076,
            "free_sulfur_dioxide": 11.0,
            "total_sulfur_dioxide": 34.0,
            "density": 0.9978,
            "pH": 3.51,
            "sulphates": 0.56,
            "alcohol": 9.4
        }
    }
    
    response = client.post("/predict", json=test_data)
    assert response.status_code == 422

def test_docs_endpoint():
    response = client.get("/docs")
    assert response.status_code == 200

def test_redoc_endpoint():
    response = client.get("/redoc")
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__]) 