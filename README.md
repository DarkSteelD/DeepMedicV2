# ITMO_Final_Project

# Wine Quality Prediction ML Pipeline

## Project Overview

This project implements an automated ML pipeline for wine quality prediction using:
- **MLflow** for experiment tracking
- **Apache Airflow** for pipeline automation  
- **DVC** for data versioning (configured separately)
- **Docker Compose** for containerized deployment

## Data
Dataset: UCI Wine Quality (red)  
File location: `data/raw/winequality-red.csv`

**Note**: DVC is configured for data versioning but runs independently of the Airflow pipeline.

## Quick Start with Docker Compose

1. **Clone and setup**:
```bash
git clone <your-repo-url>
cd itmo_final_project
```

2. **Start all services**:
```bash
docker compose up -d
```

This will start:
- **Airflow** (webserver, scheduler, worker) on http://localhost:8080
- **MLflow** tracking server on http://localhost:5000
- **PostgreSQL** and **Redis** for Airflow backend

3. **Access services**:
- Airflow UI: http://localhost:8080 (admin/admin)
- MLflow UI: http://localhost:5000

## Experiments
We use MLflow for experiment tracking with two models:

### Models and Parameters

#### RandomForest Regressor
- n_estimators: 100
- max_depth: 10
- random_state: 42

#### LightGBM
- objective: regression
- metric: mse
- num_leaves: 31
- learning_rate: 0.05
- feature_fraction: 0.9

### Metrics
- MSE (Mean Squared Error)
- R2 Score

### Latest Results
- **RandomForest**: MSE: 0.3182, R2: 0.5131
- **LightGBM**: MSE: 0.3208, R2: 0.5091

## Automation with Airflow

The `wine_quality_dag` DAG runs daily and executes both experiments automatically.

### DAG Structure
1. `train_random_forest`: Runs RandomForest experiments
2. `train_lightgbm`: Runs LightGBM experiments (after RandomForest completes)

### Manual Execution
You can trigger the DAG manually from the Airflow UI or CLI:
```bash
docker compose exec airflow-webserver airflow dags trigger wine_quality_dag
```

### Monitoring
- View experiment results in MLflow UI
- Monitor DAG execution in Airflow UI
- Check logs for debugging

## Development Setup (Local)

If you prefer to run without Docker:

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Start MLflow server**:
```bash
mlflow server --host 0.0.0.0 --port 5000
```

3. **Run experiments manually**:
```bash
python src/experiments/train.py
```

## Data Versioning (DVC)

DVC is configured for data versioning with MinIO remote storage:
- Remote: MinIO S3-compatible storage
- Configuration: `.dvc/config`
- Data files are tracked but DVC runs independently of Airflow

## Project Structure

```
├── dags/                   # Airflow DAGs
├── data/raw/              # Dataset files
├── src/experiments/       # ML training scripts
├── docker-compose.yml     # Container orchestration
├── Dockerfile            # Custom Airflow image
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Screenshots

- **Airflow DAG Overview**: Shows successful pipeline execution
- **MLflow Experiments**: Tracks model performance and parameters
- **Task Logs**: Detailed execution logs for debugging

