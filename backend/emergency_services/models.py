from enum import Enum
from pydantic import BaseModel


class ServiceType(Enum):
    GARDA = 0
    FIRE_BRIGADE = 1
    AMBULANCE = 2


class EmergencyServiceModel(BaseModel):
    id: int
    name: str
    type: ServiceType
    lat: float
    long: float
    units: int
    units_available: int
    units_busy: int
