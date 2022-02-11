from sqlalchemy.orm import Session

from .models import User, Disaster, EmergencyService
from .schemas import UserCreate, DisasterCreate, EmergencyServiceCreate, UserResponse


def get_user_by_id(db: Session, user_id: int):
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
    return db.query(Disaster).offset(skip).limit(limit).all()


def get_disaster_by_id(db: Session, id: int):
    return db.query(Disaster).filter(Disaster.id == id).first()


def add_disaster_to_db(db: Session, disaster: DisasterCreate):
    new_disaster = Disaster(
        id=disaster.disaster_id,
        type=disaster.disaster_type,
        user_id=disaster.user_id,
        scale=disaster.scale,
        latitude=disaster.lat,
        longitude=disaster.long,
    )
    db.add(new_disaster)
    db.commit()
    db.refresh(new_disaster)
    return disaster


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
