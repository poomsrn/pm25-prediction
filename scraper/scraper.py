from fastapi import FastAPI, status
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
from typing import List, Optional
import time
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy import null
import pytz
import uvicorn
import requests

# get data from .env
dotenv_path = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path)

API_ENDPOINT = os.environ.get("API_ENDPOINT")
API_PORT = os.environ.get("API_PORT")

API_URL = f"{API_ENDPOINT}:{API_PORT}"

# Init fastapi server
app = FastAPI(title='Data Sciene Project 2 Scraper')

class EarthNullBase(BaseModel):
    class Config:
        orm_mode = True

# Data schema
class Data(BaseModel):
    earthnull_timestamp : Optional[datetime.datetime] = None
    earthnull_station_id : Optional[str] = None
    earthnull_station_name : Optional[str] = None
    earthnull_region : Optional[str] = None
    earthnull_province : Optional[str] = None
    earthnull_lat : Optional[float] = None
    earthnull_long : Optional[float] = None
    earthnull_pm25 : Optional[float] = None
    earthnull_pm10 : Optional[float] = None
    earthnull_wind_dir : Optional[int] = None
    earthnull_wind_speed : Optional[int] = None
    earthnull_RH : Optional[int] = None

def waiting(driver):
    data_status = driver.find_element(By.XPATH,'/html/body/main/div[3]/div[1]/div')
    while data_status.text=="Downloading...":
        data_status = driver.find_element(By.XPATH,'/html/body/main/div[3]/div[1]/div')
        if data_status.text=="Downloading...":
            time.sleep(3)
            continue
        else :
            return
        

def insert_scrape_data(data):
    try:
        requests.adapters.DEFAULT_RETRIES = 100
        s = requests.session()
        s.keep_alive = False 
        url = 'http://localhost:8000/earthnull/insert'
        res = requests.post(url = url, json = data)
        return res.json()
    except:
        return

def insert_cleaned_data(data):
    try:
        requests.adapters.DEFAULT_RETRIES = 100
        s = requests.session()
        s.keep_alive = False 
        url = 'http://localhost:8000/cleaned_earthnull/insert'
        res = requests.post(url = url, json = data)
        return res.json()
    except:
        return

def get_lastest(station_id):
    try:
        requests.adapters.DEFAULT_RETRIES = 100
        s = requests.session()
        s.keep_alive = False 
        url = f'http://localhost:8000/cleaned_earthnull/latest-by-station/stations/{station_id}/limits/1'
        res = requests.get(url = url)
        return res.json()
    except:
        return
    
def cleaned_data(datas):
    positions = [(99.823357, 19.909242), (98.9881062, 18.7909205), (99.659873, 18.282664), (99.893048, 19.200226), (100.776359, 18.788878), (102.780926, 17.414174), (104.133216, 17.15662), (102.835251, 16.445329), (98.918138, 8.059199), (104.094535, 17.191391), (102.098301, 14.979726), (99.123056, 16.883611), (100.110542, 15.686254), (100.258056, 16.820833), (99.325355, 9.126057), (100.48404, 7.020545), (99.961469, 8.426923), (99.588743, 7.570238), (101.2831, 6.546197), (100.536443, 13.729984), (100.343164, 13.705582), (100.784069, 13.72205), (100.558606, 13.7619223), (100.785866, 13.570333), (101.286359, 13.588554), (100.977777, 13.355065), (101.098128, 13.054551), (101.180975, 12.706325), (102.523721, 12.234862)]
    station_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    province = ['เชียงราย', 'เชียงราย','เชียงใหม่','ลำปาง','พะเยา','น่าน','อุดรธานี','สกลนคร','ขอนแก่น','ร้อยเอ็ด','ศรีษะเกษ','นครราชสีมา','ตาก','นครสวรรค์','พิษณุโลก','สุราษฏ์ธานี','สงขลา','นครศรีธรรมราช','ตรัง','ยะลา','กรุงเทพฯ','กรุงเทพฯ','กรุงเทพฯ','กรุงเทพฯ','สมุทรปราการ','ฉะเชิงเทรา','ชลบุรี','ชลบุรี','ระยอง','ตราด']
    station_name = ['ต.เวียง','ต.ศรีภูมิ','ต.แม่เมาะ','ต.บ้านต๋อม','ต.ในเวียง','ต.หมากแข้ง','ต.ธาตุนาเวง','ต.ในเมือง','ต.ในเมือง','ต.เมืองเหนือ','ต.ในเมือง','ต.ระแหง','ต.ปากน้ำโพ','ต.ในเมือง','ต.มะขามเตี้ย','ต.หาดใหญ่','ต.คลัง','ต.นาตาล่วง','ต.สะเตง','เขตปทุมวัน','เขตหนองแขม','เขตลาดกระบัง','เขตดินแดง','ต.บางเสาธง','ต.วังเย็น','ต.บ้านสวน','ต.บ่อวิน','ต.เนินพระ','อ.เมือง']
    regions = ['N', 'N', 'N', 'N', 'N', 'NE', 'NE', 'NE', 'NE', 'NE', 'NE', 'W', 'W', 'W', 'S', 'S', 'S', 'S', 'S', 'C', 'C', 'C', 'C', 'C', 'E', 'E', 'E', 'E', 'E']

    strong_error = ["cleaned_earthnull_station_id", "cleaned_earthnull_station_name", "cleaned_earthnull_region", "cleaned_earthnull_province", "cleaned_earthnull_lat", "cleaned_earthnull_long"]
    soft_error = ["cleaned_earthnull_pm25", "cleaned_earthnull_pm10", "cleaned_earthnull_temp", "cleaned_earthnull_wind_dir", "cleaned_earthnull_wind_speed", "cleaned_earthnull_RH"]
    cleaned_datas = []
    for data in datas:
        flag_strong_error = False
        lastest_data = get_lastest(data["cleaned_earthnull_station_id"])
        for key in strong_error:
            if key == "cleaned_earthnull_station_id":
                if data[key] == "" or data[key] == None or data[key] not in station_id:
                    flag_strong_error = True
            elif key == "cleaned_earthnull_station_name":
                if data[key] == "" or data[key] == None or data[key] not in station_name:
                    flag_strong_error = True
            elif key == "cleaned_earthnull_region":
                if data[key] == "" or data[key] == None or data[key] not in regions:
                    flag_strong_error = True
            elif key == "cleaned_earthnull_lat":
                if data[key] == "" or data[key] == None:
                    flag_strong_error = True
            elif key == "cleaned_earthnull_long":
                if data[key] == "" or data[key] == None:
                    flag_strong_error = True
            elif key == "cleaned_earthnull_province":
                if data[key] == "" or data[key] == None or data[key] not in province:
                    flag_strong_error = True

        for key in soft_error:
            if key == "cleaned_earthnull_pm25":
                if data[key] == None and len(lastest_data) == 1:
                    data[key] = 0
                elif data[key] == None:
                    data[key] = lastest_data[0][key]
                elif data[key] > 34.5:
                    data[key] = 34.5
                elif data[key] < 0:
                    data[key] = 0
            elif key == "cleaned_earthnull_temp":
                if data[key] == None and len(lastest_data) == 0:
                    data[key] = 32
                elif data[key] == None:
                    data[key] = lastest_data[0][key]
                elif data[key] > 35.25:
                    data[key] = 35.25
                elif data[key] < 18.05:
                    data[key] = 18.05
            elif key == "cleaned_earthnull_wind_dir":
                if data[key] == None and len(lastest_data) == 0:
                    data[key] = 200
                elif data[key] == None:
                    data[key] = lastest_data[0][key]
                elif data[key] > 375:
                    data[key] = 375
                elif data[key] < 95:
                    data[key] = 95
            elif key == "cleaned_earthnull_wind_speed":
                if data[key] == None and len(lastest_data) == 0:
                    data[key] = 30
                elif data[key] == None:
                    data[key] = lastest_data[0][key]
                elif data[key] > 62:
                    data[key] = 62
                elif data[key] < 0:
                    data[key] = 0
            elif key == "cleaned_earthnull_RH":
                if data[key] == None and len(lastest_data) == 0:
                    data[key] = 60
                elif data[key] == None:
                    data[key] = lastest_data[0][key]
                elif data[key] > 118.5:
                    data[key] = 118.5
                elif data[key] < 42.5:
                    data[key] = 42.5
        if not flag_strong_error:
            cleaned_datas.append(data)
            insert_cleaned_data(data)
    return cleaned_datas


def get_day_scrape(hours_before):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
    driver.get('https://google.com/%27')
    print(driver.page_source)
    driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

    positions = [(99.823357, 19.909242), (98.9881062, 18.7909205), (99.659873, 18.282664), (99.893048, 19.200226), (100.776359, 18.788878), (102.780926, 17.414174), (104.133216, 17.15662), (102.835251, 16.445329), (98.918138, 8.059199), (104.094535, 17.191391), (102.098301, 14.979726), (99.123056, 16.883611), (100.110542, 15.686254), (100.258056, 16.820833), (99.325355, 9.126057), (100.48404, 7.020545), (99.961469, 8.426923), (99.588743, 7.570238), (101.2831, 6.546197), (100.536443, 13.729984), (100.343164, 13.705582), (100.784069, 13.72205), (100.558606, 13.7619223), (100.785866, 13.570333), (101.286359, 13.588554), (100.977777, 13.355065), (101.098128, 13.054551), (101.180975, 12.706325), (102.523721, 12.234862)]
    station_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]

    province = ['เชียงราย','เชียงใหม่','ลำปาง','พะเยา','น่าน','อุดรธานี','สกลนคร','ขอนแก่น','ร้อยเอ็ด','ศรีษะเกษ','นครราชสีมา','ตาก','นครสวรรค์','พิษณุโลก','สุราษฏ์ธานี','สงขลา','นครศรีธรรมราช','ตรัง','ยะลา','กรุงเทพฯ','กรุงเทพฯ','กรุงเทพฯ','กรุงเทพฯ','สมุทรปราการ','ฉะเชิงเทรา','ชลบุรี','ชลบุรี','ระยอง','ตราด']
    station_name = ['ต.เวียง','ต.ศรีภูมิ','ต.แม่เมาะ','ต.บ้านต๋อม','ต.ในเวียง','ต.หมากแข้ง','ต.ธาตุนาเวง','ต.ในเมือง','ต.ในเมือง','ต.เมืองเหนือ','ต.ในเมือง','ต.ระแหง','ต.ปากน้ำโพ','ต.ในเมือง','ต.มะขามเตี้ย','ต.หาดใหญ่','ต.คลัง','ต.นาตาล่วง','ต.สะเตง','เขตปทุมวัน','เขตหนองแขม','เขตลาดกระบัง','เขตดินแดง','ต.บางเสาธง','ต.วังเย็น','ต.บ้านสวน','ต.บ่อวิน','ต.เนินพระ','อ.เมือง']

    regions = ['N', 'N', 'N', 'N', 'N', 'NE', 'NE', 'NE', 'NE', 'NE', 'NE', 'W', 'W', 'W', 'S', 'S', 'S', 'S', 'S', 'C', 'C', 'C', 'C', 'C', 'E', 'E', 'E', 'E', 'E']

    # positions = [(99.823357, 19.909242)]
    # station_id = [1]
    # province = ['เชียงราย']
    # station_name = ['ต.เวียง']
    # regions = ['N']

    last_date = datetime.datetime.now(pytz.UTC)
    first_date = last_date - datetime.timedelta(hours = hours_before)
    date_collect_temp = first_date
    hours_step = 1
    while date_collect_temp < last_date:
        year = date_collect_temp.strftime("%Y")
        month = date_collect_temp.strftime("%m")
        day = date_collect_temp.strftime("%d")
        hour = date_collect_temp.strftime("%H")
        for i in range(len(positions)):
            lat = positions[i][1]
            long = positions[i][0]
            for j in range(5):
                ################ --------- Relative Humidity --------- ################
                if j == 0:
                    driver.get(f'https://earth.nullschool.net/#{year}/{month}/{day}/{hour}00Z/wind/surface/level/overlay=relative_humidity/orthographic=99.20,12.40,2283/loc={positions[i][0]},{positions[i][1]}')
                    waiting(driver)
                    data_RH = driver.find_element(By.XPATH,'//*[@id="spotlight-panel"]/div[3]/div')
                    RH_data = data_RH.text
                    if RH_data == '':
                        RH_data = None
                    else: RH_data = float(RH_data)
                
                ################ --------- PM 2.5 --------- ################
                elif j == 1:
                    driver.get(f'https://earth.nullschool.net/#{year}/{month}/{day}/{hour}00Z/particulates/surface/level/overlay=pm2.5/orthographic=99.20,12.40,2283/loc={positions[i][0]},{positions[i][1]}')
                    waiting(driver)
                    data_pm25 = driver.find_element(By.XPATH,'//*[@id="spotlight-panel"]/div[3]/div')
                    pm25_data = data_pm25.text
                    if pm25_data == '':
                        pm25_data = None
                    else: pm25_data = float(pm25_data)

                ################ --------- PM 10 --------- ################
                elif j == 2:
                    driver.get(f'https://earth.nullschool.net/#{year}/{month}/{day}/{hour}00Z/particulates/surface/level/overlay=pm10/orthographic=99.20,12.40,2283/loc={positions[i][0]},{positions[i][1]}')
                    waiting(driver)
                    data_pm10 = driver.find_element(By.XPATH,'//*[@id="spotlight-panel"]/div[3]/div')
                    pm10_data = data_pm10.text
                    if pm10_data == '':
                        pm10_data = None
                    else: pm10_data = float(pm10_data)
                
                ################ --------- Wind --------- ################
                elif j == 3:
                    driver.get(f'https://earth.nullschool.net/#{year}/{month}/{day}/{hour}00Z/wind/isobaric/850hPa/orthographic=99.20,12.40,2283/loc={positions[i][0]},{positions[i][1]}')
                    waiting(driver)
                    data_wind = driver.find_element(By.XPATH, '//*[@id="spotlight-panel"]/div[2]/div')
                    wind_data = data_wind.text
                    if wind_data.split("° @ ").__len__()!=2:
                        wind_dir =''
                        wind_speed=''
                    else :
                        wind_dir = wind_data.split("° @ ")[0]
                        wind_speed = wind_data.split("° @ ")[1]

                    if wind_dir == '' or wind_speed == '':
                        wind_dir = None
                        wind_speed = None
                    else: 
                        wind_dir = float(wind_dir)
                        wind_speed = float(wind_speed)
                
                ################ --------- Temperature --------- ################
                else:
                    driver.get(f'https://earth.nullschool.net/#{year}/{month}/{day}/{hour}00Z/wind/surface/level/overlay=temp/orthographic=99.20,12.40,2283/loc={positions[i][0]},{positions[i][1]}')
                    waiting(driver)
                    data_temp = driver.find_element(By.XPATH,'//*[@id="spotlight-panel"]/div[3]/div')
                    temp_data = data_temp.text

                    if temp_data == '':
                        temp_data = None
                    else: temp_data = float(temp_data)
            
            scrape_data = {
                "earthnull_timestamp": f'{year}-{month}-{day.zfill(2)}T{hour}:00:00.00',
                "earthnull_station_id": station_id[i],
                "earthnull_station_name": station_name[i],
                "earthnull_region": regions[i],
                "earthnull_province": province[i],
                "earthnull_lat": lat,
                "earthnull_long": long,
                "earthnull_pm25": pm25_data,
                "earthnull_pm10": pm10_data,
                "earthnull_temp": temp_data,
                "earthnull_wind_dir": wind_dir,
                "earthnull_wind_speed": wind_speed,
                "earthnull_RH": RH_data
            }

            insert_scrape_data(scrape_data)
        hours_added = datetime.timedelta(hours = hours_step)
        date_collect_temp = date_collect_temp + hours_added

    return 

def get_scrape_data():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
    driver.get('https://google.com/%27')
    print(driver.page_source)
    driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

    positions = [(99.823357, 19.909242), (98.9881062, 18.7909205), (99.659873, 18.282664), (99.893048, 19.200226), (100.776359, 18.788878), (102.780926, 17.414174), (104.133216, 17.15662), (102.835251, 16.445329), (98.918138, 8.059199), (104.094535, 17.191391), (102.098301, 14.979726), (99.123056, 16.883611), (100.110542, 15.686254), (100.258056, 16.820833), (99.325355, 9.126057), (100.48404, 7.020545), (99.961469, 8.426923), (99.588743, 7.570238), (101.2831, 6.546197), (100.536443, 13.729984), (100.343164, 13.705582), (100.784069, 13.72205), (100.558606, 13.7619223), (100.785866, 13.570333), (101.286359, 13.588554), (100.977777, 13.355065), (101.098128, 13.054551), (101.180975, 12.706325), (102.523721, 12.234862)]
    station_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]

    province = ['เชียงราย','เชียงใหม่','ลำปาง','พะเยา','น่าน','อุดรธานี','สกลนคร','ขอนแก่น','ร้อยเอ็ด','ศรีษะเกษ','นครราชสีมา','ตาก','นครสวรรค์','พิษณุโลก','สุราษฏ์ธานี','สงขลา','นครศรีธรรมราช','ตรัง','ยะลา','กรุงเทพฯ','กรุงเทพฯ','กรุงเทพฯ','กรุงเทพฯ','สมุทรปราการ','ฉะเชิงเทรา','ชลบุรี','ชลบุรี','ระยอง','ตราด']
    station_name = ['ต.เวียง','ต.ศรีภูมิ','ต.แม่เมาะ','ต.บ้านต๋อม','ต.ในเวียง','ต.หมากแข้ง','ต.ธาตุนาเวง','ต.ในเมือง','ต.ในเมือง','ต.เมืองเหนือ','ต.ในเมือง','ต.ระแหง','ต.ปากน้ำโพ','ต.ในเมือง','ต.มะขามเตี้ย','ต.หาดใหญ่','ต.คลัง','ต.นาตาล่วง','ต.สะเตง','เขตปทุมวัน','เขตหนองแขม','เขตลาดกระบัง','เขตดินแดง','ต.บางเสาธง','ต.วังเย็น','ต.บ้านสวน','ต.บ่อวิน','ต.เนินพระ','อ.เมือง']

    regions = ['N', 'N', 'N', 'N', 'N', 'NE', 'NE', 'NE', 'NE', 'NE', 'NE', 'W', 'W', 'W', 'S', 'S', 'S', 'S', 'S', 'C', 'C', 'C', 'C', 'C', 'E', 'E', 'E', 'E', 'E']

    # positions = [(99.823357, 19.909242)]
    # station_id = [1]
    # province = ['เชียงราย']
    # station_name = ['ต.เวียง']
    # regions = ['N']
    last_date = datetime.datetime.now(pytz.UTC)
    status_return = []
    clean_datas = []

    year = last_date.strftime("%Y")
    month = last_date.strftime("%m")
    day = last_date.strftime("%d")
    hour = last_date.strftime("%H")
    for i in range(len(positions)):
        lat = positions[i][1]
        long = positions[i][0]
        for j in range(5):
            ################ --------- Relative Humidity --------- ################
            if j == 0:
                driver.get(f'https://earth.nullschool.net/#{year}/{month}/{day}/{hour}00Z/wind/surface/level/overlay=relative_humidity/orthographic=99.20,12.40,2283/loc={positions[i][0]},{positions[i][1]}')
                waiting(driver)
                data_RH = driver.find_element(By.XPATH,'//*[@id="spotlight-panel"]/div[3]/div')
                RH_data = data_RH.text
                if RH_data == '':
                    RH_data = None
                else: RH_data = float(RH_data)
            
            ################ --------- PM 2.5 --------- ################
            elif j == 1:
                driver.get(f'https://earth.nullschool.net/#{year}/{month}/{day}/{hour}00Z/particulates/surface/level/overlay=pm2.5/orthographic=99.20,12.40,2283/loc={positions[i][0]},{positions[i][1]}')
                waiting(driver)
                data_pm25 = driver.find_element(By.XPATH,'//*[@id="spotlight-panel"]/div[3]/div')
                pm25_data = data_pm25.text
                if pm25_data == '':
                    pm25_data = None
                else: pm25_data = float(pm25_data)

            ################ --------- PM 10 --------- ################
            elif j == 2:
                driver.get(f'https://earth.nullschool.net/#{year}/{month}/{day}/{hour}00Z/particulates/surface/level/overlay=pm10/orthographic=99.20,12.40,2283/loc={positions[i][0]},{positions[i][1]}')
                waiting(driver)
                data_pm10 = driver.find_element(By.XPATH,'//*[@id="spotlight-panel"]/div[3]/div')
                pm10_data = data_pm10.text
                if pm10_data == '':
                    pm10_data = None
                else: pm10_data = float(pm10_data)
            
            ################ --------- Wind --------- ################
            elif j == 3:
                driver.get(f'https://earth.nullschool.net/#{year}/{month}/{day}/{hour}00Z/wind/isobaric/850hPa/orthographic=99.20,12.40,2283/loc={positions[i][0]},{positions[i][1]}')
                waiting(driver)
                data_wind = driver.find_element(By.XPATH, '//*[@id="spotlight-panel"]/div[2]/div')
                wind_data = data_wind.text
                if wind_data.split("° @ ").__len__()!=2:
                    wind_dir =''
                    wind_speed=''
                else :
                    wind_dir = wind_data.split("° @ ")[0]
                    wind_speed = wind_data.split("° @ ")[1]

                if wind_dir == '' or wind_speed == '':
                    wind_dir = None
                    wind_speed = None
                else: 
                    wind_dir = float(wind_dir)
                    wind_speed = float(wind_speed)
            
            ################ --------- Temperature --------- ################
            else:
                driver.get(f'https://earth.nullschool.net/#{year}/{month}/{day}/{hour}00Z/wind/surface/level/overlay=temp/orthographic=99.20,12.40,2283/loc={positions[i][0]},{positions[i][1]}')
                waiting(driver)
                data_temp = driver.find_element(By.XPATH,'//*[@id="spotlight-panel"]/div[3]/div')
                temp_data = data_temp.text

                if temp_data == '':
                    temp_data = None
                else: temp_data = float(temp_data)
        
        scrape_data = {
            "earthnull_timestamp": f'{year}-{month}-{day.zfill(2)}T{hour}:00:00.00',
            "earthnull_station_id": station_id[i],
            "earthnull_station_name": station_name[i],
            "earthnull_region": regions[i],
            "earthnull_province": province[i],
            "earthnull_lat": lat,
            "earthnull_long": long,
            "earthnull_pm25": pm25_data,
            "earthnull_pm10": pm10_data,
            "earthnull_temp": temp_data,
            "earthnull_wind_dir": wind_dir,
            "earthnull_wind_speed": wind_speed,
            "earthnull_RH": RH_data
        }

        status_scrape = insert_scrape_data(scrape_data)
        status_return.append(status_scrape)

        clean_data = {
            "cleaned_earthnull_timestamp": f'{year}-{month}-{day.zfill(2)}T{hour}:00:00.00',
            "cleaned_earthnull_station_id": station_id[i],
            "cleaned_earthnull_station_name": station_name[i],
            "cleaned_earthnull_region": regions[i],
            "cleaned_earthnull_province": province[i],
            "cleaned_earthnull_lat": lat,
            "cleaned_earthnull_long": long,
            "cleaned_earthnull_pm25": pm25_data,
            "cleaned_earthnull_pm10": pm10_data,
            "cleaned_earthnull_temp": temp_data,
            "cleaned_earthnull_wind_dir": wind_dir,
            "cleaned_earthnull_wind_speed": wind_speed,
            "cleaned_earthnull_RH": RH_data
        }

        clean_datas.append(clean_data)

    cleaned_data(clean_datas)

    return status_return

@app.get("/scrape-data-by-hours")
async def scrape_by_hours(hours:int):
    status_return = get_day_scrape(hours)
    return status_return


# api for get lastest data -> inference the data -> insert prediction's result to database
@app.get("/scrape-data")
async def scrape_data():
    status_return = get_scrape_data()
    return status_return

if __name__ == "__main__":
    uvicorn.run(app, port=9000, host='0.0.0.0')
