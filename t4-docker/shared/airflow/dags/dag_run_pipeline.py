from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

#establishing the default args
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
}

#creates the scheudle for the dag runs
with DAG(
    "dag_run_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 4, 12),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    
    #this bash operator runs the run pipeline file
    dag_run_pipeline_script = BashOperator(
    task_id='dag_run_pipeline',
    bash_command='python3 "/home/t4/run_pipeline.py"',
    cwd='/home/t4', 
    dag=dag,
)
