from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from app.database import init_db
from sqlalchemy.orm import Session
from app.schemas.predicted import PredictedAttribute
from app.crud.predicted import insert_predicted, get_all_predicted, get_latest_predicted_by_station


router = APIRouter(
    prefix = "/predicted",
    tags = ["Predicted"],
    responses = {404 : {'message' : 'Not found'}}
)

get_db = init_db.get_db

@router.post("/insert", response_model=PredictedAttribute, status_code=status.HTTP_201_CREATED)
async def insert_predicted_data(request:PredictedAttribute, db:Session = Depends(get_db)):
    return insert_predicted(request, db)


@router.get("/all", response_model = List[PredictedAttribute])
async def get_all_predicted_data(db:Session = Depends(get_db)):
    return get_all_predicted(db)

@router.get("/latest-by-station/stations/{station_id}")
async def get_latest_predicted_data_by_station(station_id:str, db:Session = Depends(get_db)):
    return get_latest_predicted_by_station(24, station_id, db)

