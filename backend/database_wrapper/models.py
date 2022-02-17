from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum
from enum import Enum as PyEnum
from .database import Base
from backend.emergency_services import ServiceType


class DisasterType(PyEnum):
    FIRE = 0
    FLOOD = 1
    ROAD_INCIDENT = 2
    PUBLIC_DISTRURBANCE = 3


class CivilianUser(Base):
    __tablename__ = "civilian_users"
    id = Column(String, primary_key=True, index=True)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(50))
    is_active = Column(Boolean, default=True)


class Disaster(Base):
    __tablename__ = "disasters"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(Enum(DisasterType), unique=False, index=True)
    user_id_civilian = Column(
        String,
        ForeignKey(CivilianUser.id),
        unique=False,
        index=True,
    )
    user_id_emergency = Column(
        String,
        ForeignKey(User.id),
        unique=False,
        index=True,
    )
    scale = Column(Integer, unique=False, index=True)
    latitude = Column(Float, unique=False)
    longitude = Column(Float, unique=False)


class EmergencyService(Base):
    __tablename__ = "emergency_services"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, index=True)
    type = Column(Enum(ServiceType), index=True)
    lat = Column(Float)
    long = Column(Float)
    number_fire_engines = Column(Integer)
    number_ambulances = Column(Integer)
    number_armed_units = Column(Integer)
    number_squad_car = Column(Integer)
    number_armoured_car = Column(Integer)
    number_personnel = Column(Integer)
