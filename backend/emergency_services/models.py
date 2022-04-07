from enum import Enum
from pydantic import BaseModel


class ServiceType(Enum):
    GARDA = 0
    FIRE_BRIGADE = 1
    AMBULANCE = 2
    ARMY = 3


class EmergencyServiceModel(BaseModel):
    name: str
    type: ServiceType
    lat: float
    long: float
    units: int
    units_available: int
    units_busy: int


class EmergencyServiceResponse(EmergencyServiceModel):
    id: int

    class Config:
        orm_mode = True


class EmergencyServiceUpdate(BaseModel):
    es_id: int
    units_allocated: int
