from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from app.database import init_db
from sqlalchemy.orm import Session
from app.schemas.cleaned_earthnull import CleanedEarthNullAttribute
from app.crud.cleaned_earthnull import insert_cleaned_earthnull, get_all_cleaned_earthnull, get_latest_cleaned_earthnull_by_station, get_all_cleaned_earthnull_by_station, get_n_latest_cleaned_earthnull_by_station


router = APIRouter(
    prefix = "/cleaned_earthnull",
    tags = ["CleanedEarthNull"],
    responses = {404 : {'message' : 'Not found'}}
)

get_db = init_db.get_db

@router.post("/insert", response_model=CleanedEarthNullAttribute, status_code=status.HTTP_201_CREATED)
async def insert_cleaned_earthnull_data(request:CleanedEarthNullAttribute, db:Session = Depends(get_db)):
    return insert_cleaned_earthnull(request, db)


@router.get("/all", response_model = List[CleanedEarthNullAttribute])
async def get_all_cleaned_earthnull_data(db:Session = Depends(get_db)):
    return get_all_cleaned_earthnull(db)

@router.get("/all-by-station/stations/{station_id}")
async def get_all_cleaned_earthnull_data_by_station(station_id:str, db:Session = Depends(get_db)):
    return get_all_cleaned_earthnull_by_station(station_id, db)

@router.get("/latest-by-station/stations/{station_id}")
async def get_latest_cleaned_earthnull_data_by_station(station_id:str, db:Session = Depends(get_db)):
    return get_latest_cleaned_earthnull_by_station(station_id, db)

@router.get("/latest-by-station/stations/{station_id}/limits/{n_limits}")
async def get_n_latest_cleaned_earthnull_data_by_station(station_id:str, n_limits:int, db:Session = Depends(get_db)):
    return get_n_latest_cleaned_earthnull_by_station(n_limits, station_id, db)

