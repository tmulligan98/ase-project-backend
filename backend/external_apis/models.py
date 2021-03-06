from pydantic import BaseModel
from enum import Enum
from typing import List


class StreetModel(BaseModel):  # External API Models
    """
    Model for a street. Contain info regarding flow on that street
    """

    coords_of_street: List[tuple]  # Coords marking out the segment of street concerned
    # NOTE: OpenAPI has a big with typed tuples :(
    speed: int  # Speed of travel on that street


class TrafficFlowModel(BaseModel):
    """
    This will contain a body of information regarding traffic flow at a point
    """

    # For now...
    streets: List[StreetModel]


class TrafficSources(Enum):
    TOMTOM = "tomtom"
    # Add more as they come
