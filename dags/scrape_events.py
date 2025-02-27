import datetime
from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.empty import EmptyOperator 


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'scrape_events',
    default_args=default_args,
    description='Scrape UFC events',
    schedule_interval=None,  # Disable automatic scheduling
    start_date=datetime.datetime(2024, 1, 1),
    catchup=False,
    tags=['scrapy'],
)

scrape_events = DockerOperator(
    task_id='scrape_events',
    image='ufc-data-project-2-scrapy',
    api_version='auto',
    auto_remove='Success',
    command='scrapy crawl ufc_events',
    docker_url="unix://var/run/docker.sock",
    network_mode="ufc-data-project_default",    
    environment={
        'URI': '{{ var.value.URI }}',
    },
    dag=dag,
)

scrape_events