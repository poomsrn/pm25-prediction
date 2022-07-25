from typing import List, Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class EarthNullBase(BaseModel):
    class Config:
        orm_mode = True

class EarthNullAttribute(EarthNullBase):    
    earthnull_timestamp : Optional[datetime] = None
    earthnull_station_id : Optional[str] = None
    earthnull_station_name : Optional[str] = None
    earthnull_region : Optional[str] = None
    earthnull_province : Optional[str] = None
    earthnull_lat : Optional[float] = None
    earthnull_long : Optional[float] = None
    earthnull_pm25 : Optional[float] = None
    earthnull_pm10 : Optional[float] = None
    earthnull_temp : Optional[float] = None
    earthnull_wind_dir : Optional[int] = None
    earthnull_wind_speed : Optional[int] = None
    earthnull_RH : Optional[int] = None

