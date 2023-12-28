# Airflow with Docker Compose

--- 

These are the steps to run Airflow in a local environment with docker-compose.

This configuration is going to self contain all the Airflow components and dependencies (database, logs, scheduler,
dags, etc.).

# 0. Download Airflow docker-compose
```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.0/docker-compose.yaml'
```

# 1. Set up Airflow user
```bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

# 2. Initialize the database
```bash
docker compose up airflow-init
```

# 3. Running Airflow
```bash
docker compose up
```

# 4. Cleaning up
```bashc
docker compose down --volumes --rmi all
```