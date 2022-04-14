from backend.database_wrapper.crud import (
    add_route,
    add_route_waypoint,
    get_disaster_by_id,
    get_disaster_route_ids,
    get_route_waypoints,
    get_tracks,
    free_es_from_track_table,
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
    TransportServiceResponse,
)
from backend.disaster_assessment.disaster_assesment import NearestServices
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
    get_transport_services_db,
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
    update_disaster_verification,
    update_disaster_completion,
    DisasterVerify,
    DisasterCompletion,
)
from backend.utils import init_logger
from typing import List
import json

router = APIRouter()
logger = init_logger()


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
    """
    Return all civilian users
    """
    users = get_civ_users(db, skip=skip, limit=limit)
    return users


# ---- Non Civilian Users ----
@router.post("/users/", response_model=UserResponse)
def add_user(user: UserCreate, db: SESSION_LOCAL = Depends(get_db)):
    """
    Add an emergency services user.
    """
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


@router.post("/disaster_completion", response_model=str)
def complete_disaster(
    request: Request, body: DisasterCompletion, db: SESSION_LOCAL = Depends(get_db)
):
    """Route to update disaster to completed on the DB

    Parameters
    ----------
    body : DisasterCompletion
        A body of details relating to the disaster to update
    db : SESSION_LOCAL, optional
        The current database session
    """
    # Try and see if disaster exists in db
    disaster = get_disaster_by_id(db, body.id)
    if not disaster:
        raise HTTPException(status_code=400, detail="Disaster does not exist!")
    try:
        update_disaster_completion(db, body)
        free_es_from_track_table(body.id, db)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Error Encountered: {e}")
    return "done"


@router.post("/disaster_verification", response_model=str)
def verify_disaster(
    request: Request, body: DisasterVerify, db: SESSION_LOCAL = Depends(get_db)
):
    """Route used by emergency services to verify a disaster

    Parameters
    ----------
    body : DisasterVerify
        Body of information relating to the disaster to be verified
    db : SESSION_LOCAL, optional
        The current database session
    """

    # Try and see if disaster exists in db
    disaster = get_disaster_by_id(db, body.id)
    if not disaster:
        raise HTTPException(status_code=400, detail="Disaster does not exist!")
    try:
        update_disaster_verification(db, body)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Error Encountered: {e}")
    return "done"


@router.get("/disasters/", response_model=List[DisasterResponse])
def get_disasters(
    skip: int = 0,
    limit: int = 100,
    verified: bool = None,
    completed: bool = None,
    db: SESSION_LOCAL = Depends(get_db),
):
    """
    Get all disasters
    """
    disasters = get_disasters_from_db(
        db, skip=skip, limit=limit, verified=verified, completed=completed
    )
    return disasters


@router.post("/disasters-civ/", response_model=DisasterBase)
def add_disaster_civ(
    request: Request, disaster: DisasterCreate, db: SESSION_LOCAL = Depends(get_db)
):
    """
    Add a disaster
    """
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


# ----- Emergency and Transport Services -----
@router.get("/emergency_services/", response_model=List[EmergencyServiceResponse])
def get_emergency_services(
    skip: int = 0, limit: int = 100, db: SESSION_LOCAL = Depends(get_db)
):
    res = get_emergency_services_db(db, skip=skip, limit=limit)
    return res


@router.get("/transport_services/", response_model=List[TransportServiceResponse])
def get_transport_services(
    skip: int = 0, limit: int = 100, db: SESSION_LOCAL = Depends(get_db)
):
    res = get_transport_services_db(db, skip=skip, limit=limit)
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
    disasters_res = get_disasters_from_db(db, skip=skip, limit=limit)
    drs = []
    for dr in disasters_res:
        drs.append(json.loads(dr.json()))

    return NearestServices().get_nearest_services(db, drs)


# @router.put(
#    "/free_services/{disaster_id}",
# )
# def free_services(disaster_id, db: SESSION_LOCAL = Depends(get_db)):
#    return free_es_from_track_table(disaster_id, db=db)
