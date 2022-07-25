from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from app.database import init_db
from sqlalchemy.orm import Session
from app.schemas.earthnull import EarthNullAttribute
from app.crud.earthnull import insert_earthnull, get_all_earthnull, get_latest_earthnull_by_station, get_all_earthnull_by_station


router = APIRouter(
    prefix = "/earthnull",
    tags = ["EarthNull"],
    responses = {404 : {'message' : 'Not found'}}
)

get_db = init_db.get_db

@router.post("/insert", response_model=EarthNullAttribute, status_code=status.HTTP_201_CREATED)
async def insert_earthnull_data(request:EarthNullAttribute, db:Session = Depends(get_db)):
    return insert_earthnull(request, db)


@router.get("/all", response_model = List[EarthNullAttribute])
async def get_all_earthnull_data(db:Session = Depends(get_db)):
    return get_all_earthnull(db)

@router.get("/all-by-station/stations/{station_id}")
async def get_all_earthnull_data_by_station(station_id:str, db:Session = Depends(get_db)):
    return get_all_earthnull_by_station(station_id, db)

@router.get("/latest-by-station/stations/{station_id}")
async def get_latest_earthnull_data_by_station(station_id:str, db:Session = Depends(get_db)):
    return get_latest_earthnull_by_station(station_id, db)