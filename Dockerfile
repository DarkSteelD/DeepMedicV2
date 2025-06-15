FROM apache/airflow:2.7.0

USER root

RUN apt-get update && apt-get install -y \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create mlflow directory with proper permissions
RUN mkdir -p /mlflow && chown -R airflow:root /mlflow

USER airflow

RUN pip install --no-cache-dir \
    pandas \
    numpy \
    scikit-learn \
    lightgbm \
    mlflow==2.8.0 