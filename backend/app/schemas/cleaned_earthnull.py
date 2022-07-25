from typing import List, Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class CleanedEarthNullBase(BaseModel):
    class Config:
        orm_mode = True

class CleanedEarthNullAttribute(CleanedEarthNullBase):    
    cleaned_earthnull_timestamp : Optional[datetime] = None
    cleaned_earthnull_station_id : Optional[str] = None
    cleaned_earthnull_station_name : Optional[str] = None
    cleaned_earthnull_region : Optional[str] = None
    cleaned_earthnull_province : Optional[str] = None
    cleaned_earthnull_lat : Optional[float] = None
    cleaned_earthnull_long : Optional[float] = None
    cleaned_earthnull_pm25 : Optional[float] = None
    cleaned_earthnull_pm10 : Optional[float] = None
    cleaned_earthnull_temp : Optional[float] = None
    cleaned_earthnull_wind_dir : Optional[int] = None
    cleaned_earthnull_wind_speed : Optional[int] = None
    cleaned_earthnull_RH : Optional[int] = None

