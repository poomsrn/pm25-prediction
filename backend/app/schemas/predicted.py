from typing import List, Optional
from datetime import datetime, timedelta
from uuid import UUID
from pydantic import BaseModel


class PredictedBase(BaseModel):
    class Config:
        orm_mode = True

class PredictedAttribute(PredictedBase):
    predicted_station_id : Optional[str] = None
    predicted_start_time : Optional[datetime] = None
    predicted_timestamp : Optional[datetime] = None
    predicted_interval_length : Optional[timedelta] = None
    predicted_n_interval : Optional[int] = None
    predicted_lat : Optional[float] = None
    predicted_long : Optional[float] = None
    predicted_result : Optional[float] = None
