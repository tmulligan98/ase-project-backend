from fastapi import APIRouter, Depends, HTTPException

from backend.database_wrapper import (
    UserResponse,
    UserCreate,
    Disaster,
    EmergencyServiceCreate,
    SESSION_LOCAL,
    create_user,
    get_user_by_id,
    get_users,
    add_disaster_to_db,
    get_emergency_services_db,
    add_emergency_services,
    DisasterCreate,
    EmergencyService,
    get_disaster_by_id,
    get_disasters_from_db,
)
from typing import List

router = APIRouter()


def get_db():
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/", response_model=UserResponse)
def add_user(user: UserCreate, db: SESSION_LOCAL = Depends(get_db)):
    db_user = get_user_by_id(db, user_id=user.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return create_user(db=db, user=user)


@router.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: SESSION_LOCAL = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: SESSION_LOCAL = Depends(get_db)):
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/disasters/", response_model=List[Disaster])
def get_disasters(skip: int = 0, limit: int = 100, db: SESSION_LOCAL = Depends(get_db)):
    disasters = get_disasters_from_db(db, skip=skip, limit=limit)
    return disasters


@router.post("/disasters/", response_model=Disaster)
def add_disaster(disaster: DisasterCreate, db: SESSION_LOCAL = Depends(get_db)):
    disaster_id = get_disaster_by_id(db, id=disaster.disaster_id)
    if disaster_id:
        raise HTTPException(
            status_code=400, detail="Disaster already present in the db"
        )
    return add_disaster_to_db(db=db, disaster=disaster)


@router.get("/emergency_services/", response_model=List[EmergencyService])
def get_emergency_services(
    skip: int = 0, limit: int = 100, db: SESSION_LOCAL = Depends(get_db)
):
    ES = get_emergency_services_db(db, skip=skip, limit=limit)
    return ES


@router.post("/emergency_services/", response_model=EmergencyService)
def add_emergency_service(
    emergencyservice: EmergencyServiceCreate, db: SESSION_LOCAL = Depends(get_db)
):
    return add_emergency_services(db=db, emergencyservice=emergencyservice)
