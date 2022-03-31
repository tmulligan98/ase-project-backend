from sqlalchemy.orm import Session
from backend.emergency_services import EMERGENCY_SERVICES, TRANSPORT_SERVICES
from backend.emergency_services.models import (
    EmergencyServiceResponse,
    TransportServiceResponse,
)
from .models import (
    TransportService,
    User,
    Disaster,
    EmergencyService,
    CivilianUser,
    Route,
    Waypoint,
    KeepTrack,
)

from backend.utils import get_password_hash
from .schemas import (
    DisasterBase,
    DisasterCompletion,
    DisasterVerify,
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
    new_user = User(
        email=user.email,
        name=user.name,
        hashed_password=get_password_hash(user.password),
        id=user.user_id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserResponse(user_id=user.user_id, is_active=True)


# ----- Disasters -----


def update_disaster_verification(db: Session, disaster: DisasterVerify):
    db.query(Disaster).filter(Disaster.id == disaster.id).update(
        {"verified": True, "scale": disaster.scale, "radius": disaster.radius}
    )
    db.commit()


def update_disaster_completion(db: Session, disaster: DisasterCompletion):
    db.query(Disaster).filter(Disaster.id == disaster.id).update({"completed": True})
    db.commit()


def get_disasters_from_db(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    verified: bool = None,
    completed: bool = None,
):
    if completed is not None:
        temp = (
            db.query(Disaster)
            .filter(Disaster.completed == completed)
            .offset(skip)
            .limit(limit)
            .all()
        )
    elif verified is not None:
        temp = (
            db.query(Disaster)
            .filter(Disaster.verified == verified)
            .offset(skip)
            .limit(limit)
            .all()
        )
    elif verified is not None and completed is not None:
        temp = (
            db.query(Disaster)
            .filter(Disaster.verified == verified and Disaster.completed == completed)
            .offset(skip)
            .limit(limit)
            .all()
        )
    else:
        temp = db.query(Disaster).offset(skip).limit(limit).all()

    res = map(
        lambda x: DisasterResponse(
            id=x.id,
            disaster_type=x.type,
            scale=x.scale,
            lat=x.latitude,
            long=x.longitude,
            radius=x.radius,
            already_addressed=x.already_addressed,
            verified=x.verified,
            completed=x.completed,
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
            verified=False,
            completed=False,
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
            verified=False,
            completed=False,
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


# -----Emergency and Transport Services -----


def get_emergency_services_db(db: Session, skip: int = 0, limit: int = 100):
    temp = db.query(EmergencyService).offset(skip).limit(limit).all()

    res = list(
        map(
            lambda x: EmergencyServiceResponse(
                id=x.id,
                name=x.name,
                type=x.type,
                lat=x.lat,
                long=x.long,
                units=x.units,
                units_available=x.units_available,
                units_busy=x.units_busy,
            ),
            temp,
        )
    )

    return res


def get_transport_services_db(db: Session, skip: int = 0, limit: int = 100):
    temp = db.query(TransportService).offset(skip).limit(limit).all()

    res = list(
        map(
            lambda x: TransportServiceResponse(
                id=x.id,
                name=x.name,
                lat=x.lat,
                long=x.long,
                units=x.units,
                units_available=x.units_available,
                units_busy=x.units_busy,
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
    Utility function to add all emergency and transport services to the database
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
                units_busy=x.units_busy,
            ),
            EMERGENCY_SERVICES,
        )
    )
    db.bulk_save_objects(res)
    res = list(
        map(
            lambda x: TransportService(
                name=x.name,
                lat=x.lat,
                long=x.long,
                units=x.units,
                units_available=x.units_available,
                units_busy=x.units_busy,
            ),
            TRANSPORT_SERVICES,
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


def add_track_to_db(disaster_id: int, es_id: int, units_busy: int, db: Session):
    new_track = KeepTrack(disaster_id=disaster_id, es_id=es_id, units_busy=units_busy)
    db.add(new_track)
    db.commit()
    db.refresh(new_track)
    return


def get_tracks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(KeepTrack).offset(skip).limit(limit).all()


def get_tracks_for_a_disaster(db: Session, disaster_id: int):
    return db.query(KeepTrack).filter(KeepTrack.disaster_id == disaster_id).all()


def update_es_db(es_id: int, units_allocated: int, db: Session):
    db.query(EmergencyService).filter(EmergencyService.id == es_id).update(
        {
            EmergencyService.units_busy: EmergencyService.units_busy + units_allocated,
            EmergencyService.units_available: EmergencyService.units_available
            - units_allocated,
        },
        synchronize_session=False,
    )
    db.commit()
    return "updated es units"


def update_disaster_status(d_id: int, status: bool, db: Session):
    db.query(Disaster).filter(Disaster.id == d_id).update(
        {
            Disaster.already_addressed: status,
        },
        synchronize_session=False,
    )
    db.commit()
    return "updated disaster status"


def free_es_from_track_table(disaster_id: int, db: Session):
    data = db.query(KeepTrack).filter(KeepTrack.disaster_id == disaster_id).all()
    for row in data:
        db.query(EmergencyService).filter(EmergencyService.id == row.es_id).update(
            {
                EmergencyService.units_busy: EmergencyService.units_busy
                - row.units_busy,
                EmergencyService.units_available: EmergencyService.units_available
                + row.units_busy,
            },
            synchronize_session=False,
        )
        db.commit()
        db.query(KeepTrack).filter(KeepTrack.id == row.id).delete()
        db.commit()
        # delete the disaster after freeing the es
    db.query(Disaster).filter(Disaster.id == disaster_id).delete()
    db.commit()
    return "done freeing"
