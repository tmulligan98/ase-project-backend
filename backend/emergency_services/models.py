from enum import Enum
from pydantic import BaseModel


class ServiceType(Enum):
    GARDA = 0
    FIRE_BRIGADE = 1
    AMBULANCE = 2


class EmergencyServiceModel(BaseModel):
    name: str
    type: ServiceType
    lat: float
    long: float
    number_fire_engines: int
    number_ambulances: int
    number_armed_units: int
    number_squad_car: int
    number_armoured_car: int
    number_personnel: int


class EmergencyServiceResponse(EmergencyServiceModel):
    id: int

    class Config:
        orm_mode = True
