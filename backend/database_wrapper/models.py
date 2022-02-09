from sqlalchemy import Boolean, Column, Integer, String
from enum import Enum
from .database import Base


class DisasterType(Enum):
    FIRE = 0
    FLOOD = 1
    ROAD_INCIDENT = 2
    PUBLIC_DISTRURBANCE = 3


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
    name = Column(String(50), unique=True, index=True)


class EmergencyService(Base):
    __tablename__ = "emergency_services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    location = Column(String(50), index=True)
