from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum
from enum import Enum as PyEnum
from .database import Base
from backend.emergency_services import ServiceType


class DisasterType(PyEnum):
    FIRE = 0
    FLOOD = 1
    ROAD_INCIDENT = 2
    PUBLIC_DISTRURBANCE = 3
    BIO_HAZARD = 4
    METEOR = 5
    STORM = 6
    OTHER = 7


class CivilianUser(Base):
    __tablename__ = "civilian_users"
    id = Column(String, primary_key=True, index=True)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(80))
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
    radius = Column(Integer, unique=False)
    verified = Column(Boolean, unique=False, default=False)
    completed = Column(Boolean, unique=False, default=False)
    # routes = relationship("Route", back_populates="disasters")


class EmergencyService(Base):
    __tablename__ = "emergency_services"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, index=True)
    type = Column(Enum(ServiceType), index=True)
    lat = Column(Float)
    long = Column(Float)
    units = Column(Integer)
    units_available = Column(Integer)
    units_busy = Column(Integer)


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    disaster_id = Column(Integer, ForeignKey("disasters.id"))
    # disaster = relationship("Disasters", back_populates="routes")
    type = Column(Integer)


class Waypoint(Base):
    __tablename__ = "waypoints"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    # route = relationship("Routes", back_populates="waypoints")
    sequence = Column(Integer)
    lat = Column(Float)
    lng = Column(Float)


class KeepTrack(Base):
    __tablename__ = "keeptrack"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    disaster_id = Column(
        Integer,
        ForeignKey(Disaster.id),
    )
    es_id = Column(
        Integer,
        ForeignKey(EmergencyService.id),
    )

    units_busy = Column(Integer)
