from pydantic import BaseModel
from .models import DisasterType


class CivilianUserModel(BaseModel):
    host_name: str


class UserBase(BaseModel):
    user_id: str


class UserCreate(UserBase):
    password: str
    email: str
    name: str


class UserResponse(UserBase):
    is_active: bool

    class Config:
        orm_mode = True


class DisasterBase(BaseModel):
    lat: float
    long: float
    scale: int
    disaster_type: DisasterType
    radius: int


class DisasterCreate(DisasterBase):
    # user_id: int  # Foreign key to users table
    # disaster_id: int  # PK
    pass


class DisasterCreateEmergency(DisasterBase):
    user_id: str


class DisasterResponse(DisasterBase):
    pass

    class Config:
        orm_mode = True


class EmergencyServiceBase(BaseModel):
    name: str
    location: str


class EmergencyServiceCreate(EmergencyServiceBase):
    pass


# class EmergencyService(EmergencyServiceBase):
#     id: int

#     class Config:
#         orm_mode = True


class RouteCreate(BaseModel):
    disaster_id: int
    type: int


class WaypointCreate(BaseModel):
    sequence: int
    lat: float
    long: float
