from fastapi import FastAPI
from .database.init_db import engine
# from .models.pcd import PCD
# from .models.sfa import SFA
# from .models.traffic import Traffic
from .models.earthnull import EarthNull
from .models.cleaned_earthnull import CleanedEarthNull
from .models.predicted import Predicted

from .api import earthnull
from .api import predicted
from .api import cleaned_earthnull

EarthNull.metadata.create_all(bind=engine)
Predicted.metadata.create_all(bind=engine)


app = FastAPI(title='Data Sciene Project 2 Database Management')

app.include_router(earthnull.router)
app.include_router(predicted.router)
app.include_router(cleaned_earthnull.router)
