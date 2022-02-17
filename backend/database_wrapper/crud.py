from sqlalchemy.orm import Session

from .models import User, Disaster, EmergencyService
from .schemas import UserCreate, DisasterCreate, EmergencyServiceCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(
        email=user.email, name=user.name, disaster_id=user.disaster_id, hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_disasters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Disaster).offset(skip).limit(limit).all()


def get_disaster_by_name(db: Session, name: str):
    return db.query(Disaster).filter(Disaster.name == name).first()


def add_disaster_to_db(db: Session, disaster: DisasterCreate):
    db_user = Disaster(name=disaster.name, latitude=disaster.latitude, longitude=disaster.longitude)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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
