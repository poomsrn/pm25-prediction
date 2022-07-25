from sqlalchemy import  Column, String, DateTime, Float, Integer, Boolean
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from ..database.init_db import Base

class EarthNull(Base):
    __tablename__ = "earthnull"
    
    earthnull_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    earthnull_station_id = Column(String)
    earthnull_timestamp = Column(DateTime)
    earthnull_station_name = Column(String)
    earthnull_region = Column(String)
    earthnull_province = Column(String)    
    earthnull_lat = Column(Float)
    earthnull_long = Column(Float)
    earthnull_pm25 = Column(Float)
    earthnull_pm10 = Column(Float)
    earthnull_temp = Column(Float)
    earthnull_wind_dir = Column(Integer)
    earthnull_wind_speed = Column(Integer)
    earthnull_RH = Column(Integer)
