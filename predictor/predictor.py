from fastapi import FastAPI
from fastapi import status
from dotenv import load_dotenv, find_dotenv
from tensorflow import keras
import requests
import os
import pandas as pd
import joblib
import numpy as np
from datetime import timedelta
from datetime import datetime
from dateutil import parser

# Get data from .env
dotenv_path = os.path.join('.env')
load_dotenv(dotenv_path)

API_ENDPOINT = os.environ.get("API_ENDPOINT")
API_PORT = os.environ.get("API_PORT")

# Create database endpoint from .env
API_URL = f"http://{API_ENDPOINT}:{API_PORT}"
# API_URL = "http://localhost:8000"

# Init fastapi server
app = FastAPI(title='Data Sciene Project 2 Predictor')

# Model constraints
TS = 72
INTERVAL = timedelta(hours=1)
N_INTERVALS = 24

# Demo model class
class Model:
    def __init__(self) -> None:
        self.scaler = joblib.load('./data/scaler.save')
        self.yscaler = joblib.load('./data/yscaler.save')
        self.model = keras.models.load_model('./data/my_model.h5')

    def transform(self, data):
        return self.scaler.transform(data)
    
    def inverse_transform(self, data):
        return self.yscaler.inverse_transform(data)
    
    def predict(self, data):
        return self.model.predict(data)

# Init model
model = Model()

# Insert prediction result to database
def insert_data(data):
    url = API_URL + "/predicted/insert"
    res = requests.post(url=url, json=data)
    print(res.json())

# Get latest data
def get_latest_data(station_id:str):
    url = API_URL + "/cleaned_earthnull/latest-by-station/stations/"
    url += station_id + "/limits/" + str(TS) # get latest 72 time stamps
    req = requests.get(url=url)
    return req


# Api for get lastest data -> Inference the data -> Insert prediction's result to database
@app.get("/predict-and-insert")
async def predict_and_insert():
    # For loop each station
    
    for station_id in range(1, 30):
        
        # Prepare data for predict
        data = get_latest_data(str(station_id))  
        if (data == ""):
            return status.HTTP_417_EXPECTATION_FAILED    
        
        # Create dataframe 
        df = pd.DataFrame(data.json())
        
        if (df.shape[0] < 72):
            return status.HTTP_406_NOT_ACCEPTABLE
        
        # Get present data
        df_present = df.iloc[0]
        
        df_selected = df[['cleaned_earthnull_temp', 'cleaned_earthnull_wind_speed', 'cleaned_earthnull_wind_dir',
                        'cleaned_earthnull_RH', 'cleaned_earthnull_pm25', 'cleaned_earthnull_station_id']]
        
        # Inverse data since api gave desc order of data
        df_selected_inverse = df_selected.iloc[::-1]
        
        # Scale data with minmax scaler
        df_scale = model.transform(df_selected_inverse)      
        
        # Format data to np.array
        df_format = np.array([df_scale])
        
        # Inferencing
        predicted = model.predict(df_format)
        
        result = model.inverse_transform(predicted)

        start_time = parser.parse(df_present['cleaned_earthnull_timestamp'])
        current_time = parser.parse(df_present['cleaned_earthnull_timestamp'])

        for i in range(N_INTERVALS):
            data_schema = {
                "predicted_station_id": df_present["cleaned_earthnull_station_id"],
                "predicted_start_time": str(start_time),
                "predicted_timestamp": str(current_time),
                "predicted_interval_length": str(INTERVAL),
                "predicted_n_interval": N_INTERVALS,
                "predicted_lat": df_present["cleaned_earthnull_lat"],
                "predicted_long": df_present["cleaned_earthnull_long"],
                "predicted_result": float(result[0, i])
            }
            current_time += INTERVAL
            
            # Insert predicted data to database
            insert_data(data_schema)
            
        return "Might be OK"
