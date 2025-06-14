import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import lightgbm as lgb
import mlflow
import os
import joblib

def load_data():
    df = pd.read_csv('data/raw/winequality-red.csv')
    X = df.drop('quality', axis=1)
    y = df['quality']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_rf(X_train, X_test, y_train, y_test, params):
    with mlflow.start_run(run_name="RandomForest"):
        mlflow.log_params(params)
        model = RandomForestRegressor(**params)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mlflow.log_metrics({"mse": mse, "r2": r2})
        joblib.dump(model, "rf_model.pkl")
        mlflow.log_artifact("rf_model.pkl")
        return model, mse, r2

def train_lgb(X_train, X_test, y_train, y_test, params):
    with mlflow.start_run(run_name="LightGBM"):
        mlflow.log_params(params)
        train_data = lgb.Dataset(X_train, label=y_train)
        model = lgb.train(params, train_data)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mlflow.log_metrics({"mse": mse, "r2": r2})
        model.save_model("lgb_model.txt")
        mlflow.log_artifact("lgb_model.txt")
        return model, mse, r2

if __name__ == "__main__":
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("wine_quality")

    X_train, X_test, y_train, y_test = load_data()

    rf_params = {
        "n_estimators": 100,
        "max_depth": 10,
        "random_state": 42
    }

    lgb_params = {
        "objective": "regression",
        "metric": "mse",
        "num_leaves": 31,
        "learning_rate": 0.05,
        "feature_fraction": 0.9
    }

    rf_model, rf_mse, rf_r2 = train_rf(X_train, X_test, y_train, y_test, rf_params)
    lgb_model, lgb_mse, lgb_r2 = train_lgb(X_train, X_test, y_train, y_test, lgb_params)

    print(f"RandomForest - MSE: {rf_mse:.4f}, R2: {rf_r2:.4f}")
    print(f"LightGBM - MSE: {lgb_mse:.4f}, R2: {lgb_r2:.4f}") 