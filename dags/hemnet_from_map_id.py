import pendulum
from airflow.models import Variable
from airflow import DAG
from airflow.operators.python import PythonOperator

from hemnet_loop import hemnet_loop

#initialize the dag
with DAG(
    dag_id='Hemnet_from_map_id',
    start_date= pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule_interval='0 8 * * *',
    tags=['Hemnet Scraping'],
    catchup=False
) as dag:
    #get the right stored list of map ids and call the external loop python
    def extract(**context):
        exec_date=context['logical_date']
        hemnet_loop(exec_date)

    #run the task
    extract_task=PythonOperator(
        task_id='Scrape_Hemnet',
        python_callable=extract,
        provide_context=True,
    )

    extract_task
    
