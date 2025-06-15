from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'wine_quality_dag',
    default_args=default_args,
    description='Wine Quality ML Experiments DAG',
    schedule=timedelta(days=1),
    catchup=False,
    tags=['wine', 'mlflow', 'experiments'],
)

PROJECT_PATH = '/opt/airflow/project'

base_command = f'cd {PROJECT_PATH} && PYTHONPATH={PROJECT_PATH} python -c'

train_rf = BashOperator(
    task_id='train_random_forest',
    bash_command=f'{base_command} "from src.experiments.train import run_rf_experiment; run_rf_experiment()"',
    dag=dag,
)

train_lgb = BashOperator(
    task_id='train_lightgbm',
    bash_command=f'{base_command} "from src.experiments.train import run_lgb_experiment; run_lgb_experiment()"',
    dag=dag,
)

train_rf >> train_lgb 