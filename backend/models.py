from sqlalchemy import Boolean, Column, Integer, String

from backend.database import Base


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
