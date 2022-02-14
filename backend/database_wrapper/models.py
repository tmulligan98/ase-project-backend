from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum
from enum import Enum as PyEnum
from .database import Base


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

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(50))
    is_active = Column(Boolean, default=True)


class Disaster(Base):
    __tablename__ = "disasters"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(DisasterType), unique=False, index=True)
    user_id = Column(
        String,
        ForeignKey(CivilianUser.id),
        unique=False,
        index=True,
    )
    scale = Column(Integer, unique=False, index=True)
    latitude = Column(Float, unique=False)
    longitude = Column(Float, unique=False)


class EmergencyService(Base):
    __tablename__ = "emergency_services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    location = Column(String(50), index=True)
