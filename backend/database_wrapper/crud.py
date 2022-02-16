from sqlalchemy.orm import Session

from .models import User, Disaster, EmergencyService, CivilianUser
from .schemas import (
    UserCreate,
    DisasterCreate,
    EmergencyServiceCreate,
    UserResponse,
    DisasterResponse,
    CivilianUserModel,
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


def get_disasters_from_db(db: Session, skip: int = 0, limit: int = 100):
    temp = db.query(Disaster).offset(skip).limit(limit).all()
    res = map(
        lambda x: DisasterResponse(
            disaster_type=x.type,
            scale=x.scale,
            lat=x.latitude,
            long=x.longitude,
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
        )
    db.add(new_disaster)
    db.commit()
    db.refresh(new_disaster)
    return DisasterResponse(
        disaster_type=disaster.disaster_type,
        scale=disaster.scale,
        lat=disaster.lat,
        long=disaster.long,
    )


def get_emergency_services_db(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EmergencyService).offset(skip).limit(limit).all()


def add_emergency_services(db: Session, emergencyservice: EmergencyServiceCreate):
    db_user = EmergencyService(
        name=emergencyservice.name, location=emergencyservice.location
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
