from pydantic import BaseModel
from .models import DisasterType


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class DisasterBase(BaseModel):
    pass


class DisasterCreate(DisasterBase):
    user_id: str  # Foreign key to users table
    disaster_id: str  # PK
    lat: float
    long: float
    scale: int
    disaster_type: DisasterType


class Disaster(DisasterBase):
    disaster_id: int

    class Config:
        orm_mode = True


class EmergencyServiceBase(BaseModel):
    name: str
    location: str


class EmergencyServiceCreate(EmergencyServiceBase):
    pass


class EmergencyService(EmergencyServiceBase):
    id: int

    class Config:
        orm_mode = True
