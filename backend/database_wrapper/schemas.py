from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str
    disaster_id: int


class UserCreate(UserBase):
    password: str
    disaster_id: int


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class DisasterBase(BaseModel):
    disaster_type: str
    latitude: str
    longitude: str


class DisasterCreate(DisasterBase):
    pass


class Disaster(DisasterBase):
    id: int

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
