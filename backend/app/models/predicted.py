from sqlalchemy import  Column, String, DateTime, Float, Integer, Boolean, Interval
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from ..database.init_db import Base

class Predicted(Base):
    __tablename__ = "predicted"
    
    predicted_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    predicted_station_id = Column(String)
    predicted_start_time = Column(DateTime)
    predicted_timestamp = Column(DateTime)
    predicted_interval_length = Column(Interval)
    predicted_n_interval = Column(Integer)
    predicted_lat = Column(Float)
    predicted_long = Column(Float)
    predicted_result = Column(String)
