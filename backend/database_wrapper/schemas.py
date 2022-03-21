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


class DisasterVerify(BaseModel):
    id: int
    scale: int
    radius: int


class DisasterCompletion(BaseModel):
    id: int
    complete: bool


class DisasterResponse(DisasterBase):
    id: int
    verified: bool
    completed: bool

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


class RouteBase(BaseModel):
    disaster_id: int
    type: int


class RouteCreate(RouteBase):
    pass


class RouteResponse(RouteBase):
    id: int


class WaypointBase(BaseModel):
    route_id: int
    sequence: int
    lat: float
    lng: float


class WaypointCreate(WaypointBase):
    pass


class WaypointResponse(WaypointBase):
    pass


class KeepTrackBase(BaseModel):
    disaster_id: int
    es_id: int
    units_busy: int


class KeepTrackCreate(KeepTrackBase):
    pass


class KeepTrackResponse(KeepTrackBase):
    pass
