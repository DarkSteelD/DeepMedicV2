FROM apache/airflow:2.7.0

USER root

# Keep airflow user with standard UID, but use flexible permissions
RUN usermod -u 50000 airflow

RUN apt-get update && apt-get install -y \
    libgomp1 \
    git \
    sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Allow airflow user to use sudo for permission fixes
RUN echo "airflow ALL=(ALL) NOPASSWD: /bin/chown, /bin/chmod" >> /etc/sudoers

# Create mlflow directory with proper permissions
RUN mkdir -p /mlflow && chown -R 50000:0 /mlflow

# Create models and reports directories
RUN mkdir -p /opt/airflow/project/models /opt/airflow/project/reports && \
    chown -R 50000:0 /opt/airflow/project/models /opt/airflow/project/reports

# Create DVC directories with proper permissions
RUN mkdir -p /opt/airflow/project/.dvc/tmp /opt/airflow/project/.dvc/cache && \
    chown -R 50000:0 /opt/airflow/project/.dvc && \
    chmod -R 755 /opt/airflow/project/.dvc

# Create volume mount directories
RUN mkdir -p /opt/airflow/dags /opt/airflow/logs /opt/airflow/plugins /opt/airflow/config

# Create universal entrypoint that works on any system
COPY <<EOF /entrypoint-dev.sh
#!/bin/bash

# Set universal permissions - world-writable for development
sudo chmod -R 777 /opt/airflow/dags /opt/airflow/logs /opt/airflow/plugins /opt/airflow/config 2>/dev/null || true

# Execute the original entrypoint with all arguments
exec /entrypoint "\$@"
EOF

RUN chmod +x /entrypoint-dev.sh

USER airflow

RUN pip install --no-cache-dir \
    pandas \
    numpy \
    scikit-learn \
    lightgbm \
    mlflow==2.8.0 \
    dvc[s3]==3.30.3

# Use the universal entrypoint
ENTRYPOINT ["/entrypoint-dev.sh"] 