from backend.database_wrapper.crud import add_route, get_disaster_route_ids
from backend.database_wrapper.models import Route
from backend.database_wrapper.schemas import (
    CivilianUserModel,
    DisasterBase,
    RouteBase,
    RouteCreate,
    RouteResponse,
)
from fastapi import APIRouter, Depends, HTTPException, Request
from backend.emergency_services import EmergencyServiceModel

from backend.database_wrapper import (
    UserResponse,
    UserCreate,
    DisasterResponse,
    EmergencyServiceCreate,
    SESSION_LOCAL,
    create_user,
    get_user_by_id,
    get_users,
    add_disaster_to_db,
    get_emergency_services_db,
    add_emergency_services,
    DisasterCreate,
    # get_disaster_by_id,
    get_disasters_from_db,
    get_civ_user_by_id,
    create_civ_user,
    get_civ_users,
    DisasterCreateEmergency,
    add_constant_services,
    get_emergency_service,
)
from typing import List

router = APIRouter()


def get_db():
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()


# ---- Civilian Users ----
@router.get("/handshake")
def handshake(request: Request, db: SESSION_LOCAL = Depends(get_db)):
    """
    Handshake with server
    """
    # Get client host
    client_host = request.client.host

    # If this host has not been seen before, add as new user
    civ = get_civ_user_by_id(db, client_host)

    if civ:
        raise HTTPException(status_code=400, detail="User already registered")
    return create_civ_user(db=db, host_name=client_host)


@router.get("/civilian-users/", response_model=List[CivilianUserModel])
def read_civ_users(
    skip: int = 0, limit: int = 100, db: SESSION_LOCAL = Depends(get_db)
):
    users = get_civ_users(db, skip=skip, limit=limit)
    return users


# ---- Non Civilian Users ----
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
def read_user(user_id: str, db: SESSION_LOCAL = Depends(get_db)):
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# ---- Disasters ----
@router.get("/disasters/", response_model=List[DisasterResponse])
def get_disasters(skip: int = 0, limit: int = 100, db: SESSION_LOCAL = Depends(get_db)):
    disasters = get_disasters_from_db(db, skip=skip, limit=limit)
    return disasters


@router.post("/disasters-civ/", response_model=DisasterBase)
def add_disaster_civ(
    request: Request, disaster: DisasterCreate, db: SESSION_LOCAL = Depends(get_db)
):
    client_host = request.client.host
    return add_disaster_to_db(
        db=db, disaster=disaster, host_name=client_host, is_civilian=True
    )


@router.post("/disasters-emrg/", response_model=DisasterResponse)
def add_disaster_emrg(
    request: Request,
    disaster: DisasterCreateEmergency,
    db: SESSION_LOCAL = Depends(get_db),
):
    return add_disaster_to_db(
        db=db, disaster=disaster, host_name=disaster.user_id, is_civilian=False
    )


# ----- Emergency Services -----
@router.get("/emergency_services/", response_model=List[EmergencyServiceModel])
def get_emergency_services(
    skip: int = 0, limit: int = 100, db: SESSION_LOCAL = Depends(get_db)
):
    res = get_emergency_services_db(db, skip=skip, limit=limit)
    return res


@router.post("/emergency_services/", response_model=EmergencyServiceModel)
def add_emergency_service(
    emergencyservice: EmergencyServiceCreate, db: SESSION_LOCAL = Depends(get_db)
):
    return add_emergency_services(db=db, emergencyservice=emergencyservice)


@router.get("/add_all_services/", response_model=str)
def add_all_services(db: SESSION_LOCAL = Depends(get_db)):
    """
    Add constant emergency services
    """
    emergency = get_emergency_service(db, id=0)
    if emergency:
        raise HTTPException(status_code=400, detail="Services already registered.")
    add_constant_services(db)
    return "done"


# ----- Routes -----


@router.post("/routes/", response_model=str)
def add_routes(route: RouteCreate, db: SESSION_LOCAL = Depends(get_db)):
    return add_route(db=db, route=route)


@router.get("/routes/{disaster_id}", response_model=List[RouteResponse])
def get_routes(disaster_id: int, db: SESSION_LOCAL = Depends(get_db)):
    res = get_disaster_route_ids(db, disaster_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Disaster not found")
    return res
