from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators import bash

bq_dataset_name = 'sample_bq_dataset'

with DAG(
    dag_id='example_oprators',
    schedule_interval='0 0 * * *',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=['operators']
) as dag:

    def printnos():
        print(1)

    run_this_last = DummyOperator(
        task_id='run_this_last'
    )

    normal_bash_operator= BashOperator(
        task_id="bashdemo",
        bash_command='echo 1'
    )

    normal_python_operator= PythonOperator(
        task_id="pythondemo",
        python_callable=printnos
    )

    make_bq_dataset = bash.BashOperator(
        task_id='make_bq_dataset',
        # Executing 'bq' command requires Google Cloud SDK which comes
        # preinstalled in Cloud Composer.
        #without defining the project id and anything the bq dataset was created
        bash_command=f'bq ls {bq_dataset_name} || bq mk {bq_dataset_name}')

    [normal_bash_operator,normal_python_operator,make_bq_dataset] >> run_this_last