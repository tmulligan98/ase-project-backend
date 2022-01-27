from typing import List, Optional

from pydantic import BaseModel


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
    name: str


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
