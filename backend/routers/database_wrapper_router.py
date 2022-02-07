from fastapi import APIRouter, Depends, HTTPException
from backend.database_wrapper import (
    User,
    UserCreate,
    Disaster,
    EmergencyServiceCreate,
    SESSION_LOCAL,
    create_user,
    get_user,
    get_users,
    get_user_by_email,
    add_disaster_to_db,
    get_emergency_services_db,
    add_emergency_services,
    get_db,
    DisasterCreate,
    EmergencyService,
    get_disaster_by_name,
)
from typing import List

router = APIRouter()


@router.post("/users/", response_model=User)
def add_user(user: UserCreate, db: SESSION_LOCAL = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@router.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: SESSION_LOCAL = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: SESSION_LOCAL = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/disasters/", response_model=List[Disaster])
def get_disasters(skip: int = 0, limit: int = 100, db: SESSION_LOCAL = Depends(get_db)):
    disasters = get_disasters(db, skip=skip, limit=limit)
    return disasters


@router.post("/disasters/", response_model=Disaster)
def add_disaster(disaster: DisasterCreate, db: SESSION_LOCAL = Depends(get_db)):
    db_user = get_disaster_by_name(db, name=disaster.name)
    if db_user:
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
