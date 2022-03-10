from backend.database_wrapper.crud import (
    add_route,
    add_route_waypoint,
    get_disaster_route_ids,
    get_route_waypoints,
    get_tracks,
)
from backend.database_wrapper.schemas import (
    CivilianUserModel,
    DisasterBase,
    RouteCreate,
    RouteResponse,
    WaypointCreate,
    WaypointResponse,
)
from fastapi import APIRouter, Depends, HTTPException, Request
from backend.emergency_services.models import (
    EmergencyServiceModel,
    EmergencyServiceResponse,
)
from backend.disaster_assessment.disaster_assesment import get_nearest_services
from backend.database_wrapper import get_db
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
import json

router = APIRouter()


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
@router.get("/emergency_services/", response_model=List[EmergencyServiceResponse])
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


@router.post("/routes/waypoints/", response_model=str)
def add_waypoint(waypoint: WaypointCreate, db: SESSION_LOCAL = Depends(get_db)):
    return add_route_waypoint(db=db, waypoint=waypoint)


@router.get("/routes/waypoints/{route_id}", response_model=List[WaypointResponse])
def get_waypoints(route_id: int, db: SESSION_LOCAL = Depends(get_db)):
    res = get_route_waypoints(db, route_id)
    if res is None:
        raise HTTPException(status_code=404, detail="No Waypoints found")
    return res


# @router.put("/update_emergency_service/")
# def update_es(request: EmergencyServiceUpdate, db: SESSION_LOCAL = Depends(get_db)):
#     return update_es_db(request, db)
#
#
# @router.post("/keep_track/")
# def add_track(track: KeepTrackCreate, db: SESSION_LOCAL = Depends(get_db)):
#     return add_track_to_db(db=db, track=track)


@router.get("/get_tracks/")
def get_all_tracks(
    skip: int = 0, limit: int = 100, db: SESSION_LOCAL = Depends(get_db)
):
    return get_tracks(db, skip=skip, limit=limit)


@router.get(
    "/get_nearest_services/",
)
def nearest_services(
    skip: int = 0, limit: int = 100, db: SESSION_LOCAL = Depends(get_db)
):
    emergency_res = get_emergency_services_db(db, skip=skip, limit=limit)
    disasters_res = get_disasters_from_db(db, skip=skip, limit=limit)

    ers = []
    for er in emergency_res:
        ers.append(json.loads(er.json()))

    drs = []
    for dr in disasters_res:
        drs.append(json.loads(dr.json()))

    return get_nearest_services(db, drs, ers)
