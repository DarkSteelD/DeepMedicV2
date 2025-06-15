#!/usr/bin/env python3
"""
Script to run the Wine Quality API server locally
"""

import os
import sys
import uvicorn

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import after path setup
from api.config import settings

if __name__ == "__main__":
    # Set environment variables for local development if not set
    os.environ.setdefault("ENVIRONMENT", "development")
    os.environ.setdefault("MLFLOW_TRACKING_URI", "http://localhost:5000")
    os.environ.setdefault("RELOAD", "true")
    
    # Run the server with configuration
    uvicorn.run(
        "api.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level
    ) 