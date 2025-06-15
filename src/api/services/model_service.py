import os
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, Tuple, Optional
import mlflow
import mlflow.sklearn
import lightgbm as lgb

from ..config import settings


class ModelService:
    def __init__(self):
        self.models_cache = {}
        self.current_model_info = {}
        
    def load_best_model(self) -> Tuple[Any, Dict[str, Any]]:
        try:
            mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
            
            experiment = mlflow.get_experiment_by_name(settings.mlflow_experiment_name)
            if not experiment:
                raise Exception(f"Experiment '{settings.mlflow_experiment_name}' not found")
            
            runs = mlflow.search_runs(
                experiment_ids=[experiment.experiment_id],
                order_by=["start_time DESC"],
                max_results=10
            )
            
            if runs.empty:
                raise Exception("No runs found in the experiment")
            
            best_run = runs.loc[runs['metrics.mse'].idxmin()]
            
            model_uri = f"runs:/{best_run.run_id}/model"
            model = mlflow.sklearn.load_model(model_uri)
            
            self.models_cache['best_model'] = model
            self.current_model_info = {
                'model_type': best_run.get('tags.model_type', 'unknown'),
                'model_version': best_run.run_id[:8],
                'training_date': best_run.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'metrics': {
                    'mse': best_run.get('metrics.mse', 0),
                    'rmse': best_run.get('metrics.rmse', 0),
                    'mae': best_run.get('metrics.mae', 0),
                    'r2': best_run.get('metrics.r2', 0)
                },
                'run_id': best_run.run_id,
                'model_path': model_uri
            }
            
            return model, self.current_model_info
            
        except Exception as e:
            print(f"MLflow loading failed: {e}. Trying local models...")
            return self._load_local_fallback_model()

    def _load_local_fallback_model(self) -> Tuple[Any, Dict[str, Any]]:
        rf_path = settings.model_rf_path
        lgb_path = settings.model_lgb_path
        
        if os.path.exists(rf_path):
            with open(rf_path, 'rb') as f:
                model = pickle.load(f)
            
            self.models_cache['best_model'] = model
            self.current_model_info = {
                'model_type': 'RandomForest',
                'model_version': 'local_fallback',
                'training_date': datetime.fromtimestamp(os.path.getmtime(rf_path)).strftime('%Y-%m-%d %H:%M:%S'),
                'metrics': {'mse': 0.0, 'rmse': 0.0, 'mae': 0.0, 'r2': 0.0},
                'run_id': 'local_fallback',
                'model_path': rf_path
            }
            return model, self.current_model_info
            
        elif os.path.exists(lgb_path):
            model = lgb.Booster(model_file=lgb_path)
            
            self.models_cache['best_model'] = model
            self.current_model_info = {
                'model_type': 'LightGBM',
                'model_version': 'local_fallback',
                'training_date': datetime.fromtimestamp(os.path.getmtime(lgb_path)).strftime('%Y-%m-%d %H:%M:%S'),
                'metrics': {'mse': 0.0, 'rmse': 0.0, 'mae': 0.0, 'r2': 0.0},
                'run_id': 'local_fallback',
                'model_path': lgb_path
            }
            return model, self.current_model_info
        
        else:
            raise Exception("No models found - neither MLflow nor local fallback models are available")

    def get_model(self) -> Tuple[Any, Dict[str, Any]]:
        if 'best_model' not in self.models_cache:
            return self.load_best_model()
        return self.models_cache['best_model'], self.current_model_info

    def is_model_loaded(self) -> bool:
        return 'best_model' in self.models_cache and self.models_cache['best_model'] is not None

    def get_model_info(self) -> Dict[str, Any]:
        if not self.is_model_loaded():
            self.load_best_model()
        return self.current_model_info.copy()

    def predict(self, features_df: pd.DataFrame) -> float:
        model, model_info = self.get_model()
        
        expected_columns = [
            "fixed_acidity", "volatile_acidity", "citric_acid", "residual_sugar",
            "chlorides", "free_sulfur_dioxide", "total_sulfur_dioxide", 
            "density", "pH", "sulphates", "alcohol"
        ]
        features_df = features_df[expected_columns]
        
        if model_info['model_type'] == 'LightGBM':
            prediction = model.predict(features_df.values)[0]
        else:
            prediction = model.predict(features_df)[0]
        
        prediction = max(0, min(10, float(prediction)))
        return prediction


model_service = ModelService() 