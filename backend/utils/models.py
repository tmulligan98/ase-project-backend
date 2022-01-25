from pydantic import BaseModel
from typing import Tuple, List


class StreetModel(BaseModel):
    """
    Model for a street. Contain info regarding flow on that street
    """

    coords_of_street: List[
        Tuple[float, float]
    ]  # Coords marking out the segment of street concerned
    speed: int  # Speed of travel on that street


class TrafficFlowModel(BaseModel):
    """
    This will contain a body of information regarding traffic flow at a point
    """

    # For now...
    streets: List[StreetModel]
