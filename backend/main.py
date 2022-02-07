import os
from typing import List

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from sqlalchemy.orm import Session

from backend import crud, models, schemas
from backend.database import SessionLocal, engine
from backend.routers import external_api_router, sample_router
from backend.utils import init_logger

load_dotenv(".env")

API_VERSION_PREFIX = "/api/1"

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

logger = init_logger()


origins = ["http://localhost:3000", "localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    DBSessionMiddleware,
    db_url=os.environ["DATABASE_URL"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def hello_world():
    return {
        "disasterStatus": True,
        "disasterLocation": {
            "longitude": 0,
            "latitude": 0,
        },
    }


@app.get("/health")
async def health_check():
    return {"status": "UP"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/disasters/", response_model=List[schemas.Disaster])
def get_disasters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    disasters = crud.get_disasters(db, skip=skip, limit=limit)
    return disasters


@app.post("/disasters/", response_model=schemas.Disaster)
def add_disaster(disaster: schemas.DisasterCreate, db: Session = Depends(get_db)):
    db_user = crud.get_disaster_by_name(db, name=disaster.name)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Disaster already present in the db"
        )
    return crud.add_disaster(db=db, disaster=disaster)


@app.get("/emergency_services/", response_model=List[schemas.EmergencyService])
def get_emergency_services(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    ES = crud.get_emergency_services(db, skip=skip, limit=limit)
    return ES


@app.post("/emergency_services/", response_model=schemas.EmergencyService)
def add_emergency_service(
    emergencyservice: schemas.EmergencyServiceCreate, db: Session = Depends(get_db)
):
    return crud.add_emergency_services(db=db, emergencyservice=emergencyservice)


app.include_router(sample_router.router, prefix=API_VERSION_PREFIX)
app.include_router(external_api_router.router, prefix=API_VERSION_PREFIX)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
