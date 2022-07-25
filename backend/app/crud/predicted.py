from fastapi import HTTPException, status
from sqlalchemy.orm import Session ,load_only
from app.models.predicted import Predicted
from app.schemas.predicted import PredictedAttribute
from datetime import datetime


def insert_predicted(request:PredictedAttribute, db:Session):
    db_predicted = Predicted(predicted_station_id = request.predicted_station_id,
                       predicted_start_time = request.predicted_start_time,
                       predicted_timestamp = request.predicted_timestamp,
                       predicted_interval_length = request.predicted_interval_length,
                       predicted_n_interval = request.predicted_n_interval,
                       predicted_lat = request.predicted_lat,
                       predicted_long = request.predicted_long,
                       predicted_result = request.predicted_result)
    db.add(db_predicted)
    db.commit()
    db.refresh(db_predicted)
    return db_predicted

def get_all_predicted(db:Session):
    return db.query(Predicted).all()

def get_latest_predicted_by_station(n_limits, station_id:str, db:Session):
    fields = ['predicted_start_time']
    start_time = db.query(Predicted).filter(
        Predicted.predicted_station_id == station_id
        ).order_by(
            Predicted.predicted_start_time.desc()
            ).with_entities(
                Predicted.predicted_start_time
                ).first()[0]
    print(start_time)
    return db.query(Predicted).filter(
        Predicted.predicted_start_time == start_time
        ).order_by(
           Predicted.predicted_timestamp.asc()).limit(n_limits).all()

