from sqlalchemy.orm import Session

from backend import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email, name=user.name, hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_disasters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Disaster).offset(skip).limit(limit).all()


def get_disaster_by_name(db: Session, name: str):
    return db.query(models.Disaster).filter(models.Disaster.name == name).first()


def add_disaster(db: Session, disaster: schemas.DisasterCreate):
    db_user = models.Disaster(name=disaster.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_emergency_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.EmergencyService).offset(skip).limit(limit).all()


def add_emergency_services(
    db: Session, emergencyservice: schemas.EmergencyServiceCreate
):
    db_user = models.EmergencyService(
        name=emergencyservice.name, location=emergencyservice.location
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
