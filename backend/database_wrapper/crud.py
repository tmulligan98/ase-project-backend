from sqlalchemy.orm import Session
from backend.emergency_services import EMERGENCY_SERVICES
from backend.emergency_services import EmergencyServiceModel
from .models import User, Disaster, EmergencyService, CivilianUser, Route, Waypoint
from .schemas import (
    DisasterBase,
    RouteCreate,
    RouteResponse,
    UserCreate,
    DisasterCreate,
    EmergencyServiceCreate,
    UserResponse,
    DisasterResponse,
    CivilianUserModel,
    WaypointCreate,
    WaypointResponse,
)


# ----- Civilian user CRUD -----
def get_civ_user_by_id(db: Session, user_id: int):
    return db.query(CivilianUser).filter(CivilianUser.id == user_id).first()


def create_civ_user(db: Session, host_name: str):
    new_user = CivilianUser(id=host_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return CivilianUserModel(host_name=host_name)


def get_civ_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(CivilianUser).offset(skip).limit(limit).all()

    res = map(
        lambda x: CivilianUserModel(
            host_name=x.id,
        ),
        users,
    )
    return list(res)


# ----- User CRUD -----
def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    new_user = User(
        email=user.email,
        name=user.name,
        hashed_password=fake_hashed_password,
        id=user.user_id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserResponse(user_id=user.user_id, is_active=True)


# ----- Disasters -----


def get_disasters_from_db(db: Session, skip: int = 0, limit: int = 100):
    temp = db.query(Disaster).offset(skip).limit(limit).all()
    res = map(
        lambda x: DisasterResponse(
            id=x.id,
            disaster_type=x.type,
            scale=x.scale,
            lat=x.latitude,
            long=x.longitude,
            radius=x.radius,
        ),
        temp,
    )
    return list(res)


def get_disaster_by_id(db: Session, id: int):
    return db.query(Disaster).filter(Disaster.id == id).first()


def add_disaster_to_db(
    db: Session, disaster: DisasterCreate, host_name: str, is_civilian: bool
):

    if is_civilian:
        new_disaster = Disaster(
            # id=disaster.disaster_id,
            type=disaster.disaster_type,
            user_id_civilian=host_name,
            scale=disaster.scale,
            latitude=disaster.lat,
            longitude=disaster.long,
            user_id_emergency=None,
            radius=disaster.radius,
        )
    else:
        new_disaster = Disaster(
            # id=disaster.disaster_id,
            type=disaster.disaster_type,
            user_id_civilian=None,
            scale=disaster.scale,
            latitude=disaster.lat,
            longitude=disaster.long,
            user_id_emergency=host_name,
            radius=disaster.radius,
        )
    db.add(new_disaster)
    db.commit()
    db.refresh(new_disaster)
    return DisasterBase(
        disaster_type=disaster.disaster_type,
        scale=disaster.scale,
        lat=disaster.lat,
        long=disaster.long,
        radius=disaster.radius,
    )


# ----- Emergency Services -----


def get_emergency_services_db(db: Session, skip: int = 0, limit: int = 100):
    temp = db.query(EmergencyService).offset(skip).limit(limit).all()

    res = list(
        map(
            lambda x: EmergencyServiceModel(
                name=x.name,
                type=x.type,
                lat=x.lat,
                long=x.long,
                units=x.units,
                units_available=x.units_available,
                units_busy=x.units_busy
            ),
            temp,
        )
    )

    return res


def add_emergency_services(db: Session, emergencyservice: EmergencyServiceCreate):
    db_user = EmergencyService(
        name=emergencyservice.name, location=emergencyservice.location
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_emergency_service(db: Session, id: int):
    return db.query(EmergencyService).filter(EmergencyService.id == id).first()


def add_constant_services(db: Session):
    """
    Utility function to add the list of emergnency services to the database
    """
    res = list(
        map(
            lambda x: EmergencyService(
                name=x.name,
                type=x.type,
                lat=x.lat,
                long=x.long,
                units=x.units,
                units_available=x.units_available,
                units_busy=x.units_busy
            ),
            EMERGENCY_SERVICES,
        )
    )
    db.bulk_save_objects(res)
    db.commit()


# ----- Routes -----


def add_route(db: Session, route: RouteCreate):
    route = Route(disaster_id=route.disaster_id, type=route.disaster_id)
    db.add(route)
    db.commit()
    db.refresh(route)
    return route.id


# get all route ids for a disaster
def get_disaster_route_ids(db: Session, disaster_id: int):
    temp = db.query(Route).filter(Disaster.id == disaster_id).all()
    res = map(
        lambda x: RouteResponse(id=x.id, disaster_id=x.disaster_id, type=x.type),
        temp,
    )
    return list(res)


def add_route_waypoint(db: Session, waypoint: WaypointCreate):
    waypoint = Waypoint(
        route_id=waypoint.route_id,
        sequence=waypoint.sequence,
        lat=waypoint.lat,
        lng=waypoint.lng,
    )
    db.add(waypoint)
    db.commit()
    db.refresh(waypoint)
    return


def get_route_waypoints(db: Session, route_id: int):
    temp = db.query(Waypoint).filter(Route.id == route_id).all()
    res = map(
        lambda x: WaypointResponse(
            route_id=x.route_id, sequence=x.sequence, lat=x.lat, lng=x.lng
        ),
        temp,
    )
    return list(res)
