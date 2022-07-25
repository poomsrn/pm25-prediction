from fastapi import HTTPException, status
from sqlalchemy.orm import Session ,load_only
from app.models.earthnull import EarthNull
from app.schemas.earthnull import EarthNullAttribute
from datetime import datetime


def insert_earthnull(request:EarthNullAttribute, db:Session):
    db_earthnull = EarthNull(earthnull_timestamp = request.earthnull_timestamp,
                        earthnull_station_id = request.earthnull_station_id,
                        earthnull_station_name = request.earthnull_station_name,
                        earthnull_region = request.earthnull_region,
                        earthnull_province = request.earthnull_province, 
                        earthnull_lat = request.earthnull_lat,
                        earthnull_long = request.earthnull_long,
                        earthnull_pm25 = request.earthnull_pm25,
                        earthnull_pm10 = request.earthnull_pm10,
                        earthnull_temp = request.earthnull_temp,
                        earthnull_wind_dir = request.earthnull_wind_dir,
                        earthnull_wind_speed = request.earthnull_wind_speed,
                        earthnull_RH = request.earthnull_RH)
    db.add(db_earthnull)
    db.commit()
    db.refresh(db_earthnull)
    return db_earthnull

def get_all_earthnull(db:Session):
    return db.query(EarthNull).all()

def get_all_earthnull_by_station(station_id:str, db:Session):
    return db.query(EarthNull).filter(EarthNull.earthnull_station_id == station_id).order_by(EarthNull.earthnull_timestamp.desc()).all()

def get_latest_earthnull_by_station(station_id:str, db:Session):
    return db.query(EarthNull).filter(EarthNull.earthnull_station_id == station_id).order_by(EarthNull.earthnull_timestamp.desc()).first()

def get_earthnull_by_date(datetime:datetime, db:Session):
    pass

def get_earthnull_by_range_date(from_date:datetime, til_date:datetime, db:Session):
    pass

def get_earthnull_by_date(datetime:datetime, db:Session):
    pass