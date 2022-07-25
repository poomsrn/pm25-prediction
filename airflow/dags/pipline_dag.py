from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os
import requests
import random
from dotenv import load_dotenv


# load_dotenv('../airflow/.env')

SCRAPER_ENDPOINT="host.docker.internal"
SCRAPER_PORT="9000"

PREDICTOR_ENDPOINT="host.docker.internal"
PREDICTOR_PORT="7000"

# SCRAPER_ENDPOINT=os.environ.get("SCRAPER_ENDPOINT")
# SCRAPER_PORT=os.environ.get("SCRAPER_PORT")

# PREDICTOR_ENDPOINT=os.environ.get("PREDICTOR_ENDPOINT")
# PREDICTOR_PORT=os.environ.get("PREDICTOR_PORT")

args = {
    'owner' : 'datasci-project2',
    'start_date' : datetime(2022, 5, 15)
}
    
def trigger_scraper():
    # url = f"http://{SCRAPER_ENDPOINT}:{SCRAPER_PORT}" + "/scrape-data" # end point path + "/"
    url = "http://host.docker.internal:9000" + "/scrape-data"
    req = requests.get(url)
    print(req.json())

def trigger_predictor():
    # url = f"http://{PREDICTOR_ENDPOINT}:{PREDICTOR_PORT}" + "/predict-and-insert" # end point path + "/"
    url = "http://host.docker.internal:7000" + "/predict-and-insert"
    req = requests.get(url)
    print(req.json())

dag = DAG(dag_id='pipline_dag', 
          default_args=args, 
          schedule_interval= '@hourly',#'*/1 * * * *', # run every 1 minute for hourly, use '@hourly'
          description='Data Pipeline for Data Science Project 2', 
          catchup=False) 

with dag:
    scraping = PythonOperator(
        task_id = 'scrape_data',
        python_callable = trigger_scraper,    
    )
    
    predicting = PythonOperator(
        task_id = 'predict_pm25',
        python_callable = trigger_predictor,
    )
    
    scraping >> predicting
    
