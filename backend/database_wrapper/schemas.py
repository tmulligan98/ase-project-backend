from pydantic import BaseModel
from .models import DisasterType


class UserBase(BaseModel):
    user_id: int


class UserCreate(UserBase):
    password: str
    email: str
    name: str


class UserResponse(UserBase):
    is_active: bool

    class Config:
        orm_mode = True


class DisasterBase(BaseModel):
    pass


class DisasterCreate(DisasterBase):
    user_id: int  # Foreign key to users table
    disaster_id: int  # PK
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
