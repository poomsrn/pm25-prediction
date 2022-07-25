from sqlalchemy import  Column, String, DateTime, Float, Integer, Boolean
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from ..database.init_db import Base

class CleanedEarthNull(Base):
    __tablename__ = "cleaned_earthnull"
    
    cleaned_earthnull_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    cleaned_earthnull_station_id = Column(String)
    cleaned_earthnull_timestamp = Column(DateTime)
    cleaned_earthnull_station_name = Column(String)
    cleaned_earthnull_region = Column(String)
    cleaned_earthnull_province = Column(String)    
    cleaned_earthnull_lat = Column(Float)
    cleaned_earthnull_long = Column(Float)
    cleaned_earthnull_pm25 = Column(Float)
    cleaned_earthnull_pm10 = Column(Float)
    cleaned_earthnull_temp = Column(Float)
    cleaned_earthnull_wind_dir = Column(Integer)
    cleaned_earthnull_wind_speed = Column(Integer)
    cleaned_earthnull_RH = Column(Integer)
