from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
import sys
import os
import subprocess
import json

# Add the project root to Python path
sys.path.append('/opt/airflow/project')

from src.experiments.train import run_rf_experiment, run_lgb_experiment

# Default arguments for the DAG
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Create the DAG
dag = DAG(
    'wine_quality_dag',
    default_args=default_args,
    description='Wine Quality Model Training Pipeline with DVC Integration',
    schedule_interval='@daily',  # Run daily
    max_active_runs=1,
    catchup=False,
    tags=['ml', 'wine-quality', 'training', 'dvc']
)

def check_dvc_status():
    """Check if there are changes in DVC tracked files"""
    try:
        os.chdir('/opt/airflow/project')
        
        # Check DVC status
        result = subprocess.run(['dvc', 'status'], 
                              capture_output=True, text=True, cwd='/opt/airflow/project')
        
        print(f"DVC status output: {result.stdout}")
        print(f"DVC status error: {result.stderr}")
        
        # If no changes, dvc status returns empty output
        if result.returncode == 0 and not result.stdout.strip():
            print("No changes detected in DVC tracked files")
            return 'skip_training'
        else:
            print("Changes detected in DVC tracked files or need to pull data")
            return 'pull_data'
            
    except Exception as e:
        print(f"Error checking DVC status: {e}")
        # In case of error, proceed with training to be safe
        return 'pull_data'

def check_data_availability():
    """Check if the wine quality dataset is available and valid"""
    data_path = '/opt/airflow/project/data/raw/winequality-red.csv'
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    
    # Check if data is not empty
    with open(data_path, 'r') as f:
        lines = f.readlines()
        if len(lines) < 2:  # At least header + 1 data row
            raise ValueError("Dataset appears to be empty or invalid")
    
    print(f"Data validation passed. Found {len(lines)-1} data rows.")
    
    # Save data info for comparison
    data_info = {
        'row_count': len(lines) - 1,
        'file_size': os.path.getsize(data_path),
        'last_modified': os.path.getmtime(data_path),
        'timestamp': datetime.now().isoformat()
    }
    
    os.makedirs('/opt/airflow/project/logs', exist_ok=True)
    with open('/opt/airflow/project/logs/data_info.json', 'w') as f:
        json.dump(data_info, f, indent=2)
    
    return True

def save_best_model():
    """Save the best performing model and commit to DVC"""
    import mlflow
    import joblib
    import json
    from mlflow.tracking import MlflowClient
    
    # Connect to MLflow
    mlflow.set_tracking_uri("http://mlflow:5000")
    client = MlflowClient()
    
    # Get the experiment
    experiment = client.get_experiment_by_name("wine_quality")
    if experiment is None:
        print("No experiment found")
        return
    
    # Get recent runs from today's experiments - fix timestamp format
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string=f"attribute.start_time >= {int(today.timestamp() * 1000)}",
        order_by=["metrics.mse ASC"]  # Best model has lowest MSE
    )
    
    if not runs:
        print("No runs found from today's experiments")
        return
    
    best_run = runs[0]
    print(f"Best run from today: {best_run.info.run_id} with MSE: {best_run.data.metrics.get('mse', 'N/A')}")
    
    # Save model metadata
    model_info = {
        'run_id': best_run.info.run_id,
        'model_name': best_run.data.tags.get('mlflow.runName', 'unknown'),
        'mse': best_run.data.metrics.get('mse'),
        'r2': best_run.data.metrics.get('r2'),
        'timestamp': datetime.now().isoformat(),
        'parameters': dict(best_run.data.params),
        'training_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    # Save metadata to models directory
    os.makedirs('/opt/airflow/project/models', exist_ok=True)
    with open('/opt/airflow/project/models/model_info.json', 'w') as f:
        json.dump(model_info, f, indent=2)
    
    print(f"Model metadata saved for run {best_run.info.run_id}")
    
    # Try to download model artifacts from MLflow
    try:
        artifact_path = client.download_artifacts(best_run.info.run_id, ".", dst_path="/opt/airflow/project/models/artifacts")
        print(f"Model artifacts downloaded to: {artifact_path}")
    except Exception as e:
        print(f"Could not download artifacts: {e}")

# Define tasks

# 1. Check DVC status to decide if we need to retrain
check_dvc_task = BranchPythonOperator(
    task_id='check_dvc_status',
    python_callable=check_dvc_status,
    dag=dag
)

# 2. Pull data from DVC if changes detected
pull_data_task = BashOperator(
    task_id='pull_data',
    bash_command='cd /opt/airflow/project && dvc pull --force',
    dag=dag
)

# 3. Validate data after pulling
check_data_task = PythonOperator(
    task_id='check_data_availability',
    python_callable=check_data_availability,
    dag=dag
)

# 4. Training tasks
train_rf_task = PythonOperator(
    task_id='train_random_forest',
    python_callable=run_rf_experiment,
    dag=dag
)

train_lgb_task = PythonOperator(
    task_id='train_lightgbm',
    python_callable=run_lgb_experiment,
    dag=dag
)

# 5. Save best model and commit to DVC
save_model_task = PythonOperator(
    task_id='save_best_model',
    python_callable=save_best_model,
    dag=dag
)

# 6. Commit new model to DVC
commit_model_task = BashOperator(
    task_id='commit_model_to_dvc',
    bash_command='''
    cd /opt/airflow/project
    dvc add models/model_info.json
    dvc add models/artifacts/ || echo "No artifacts to add"
    dvc push || echo "Push failed, but continuing"
    echo "Model committed to DVC"
    ''',
    dag=dag
)

# 7. Skip training dummy task
skip_training_task = DummyOperator(
    task_id='skip_training',
    dag=dag
)

# 8. Training complete dummy task  
training_complete_task = DummyOperator(
    task_id='training_complete',
    dag=dag,
    trigger_rule='none_failed_or_skipped'
)

# Set task dependencies
check_dvc_task >> [pull_data_task, skip_training_task]
pull_data_task >> check_data_task >> [train_rf_task, train_lgb_task]
[train_rf_task, train_lgb_task] >> save_model_task >> commit_model_task
skip_training_task >> training_complete_task
commit_model_task >> training_complete_task 