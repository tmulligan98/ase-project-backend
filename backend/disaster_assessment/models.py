from pydantic import BaseModel
from typing import List


class DisasterAssessment(BaseModel):
    ambulance: List[dict]
    police: List[dict]
    fire_brigade: List[dict]
