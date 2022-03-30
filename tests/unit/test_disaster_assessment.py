from backend.database_wrapper.schemas import DisasterResponse
from backend.disaster_assessment.disaster_assesment import NearestServices
from typing import List

from backend.emergency_services.models import EmergencyServiceResponse


def test_disaster_type(example_disaster: DisasterResponse):
    """Test the type of disaster"""
    assert example_disaster.disaster_type.__dict__["_name_"] == "ROAD_INCIDENT"
    assert not example_disaster.disaster_type.__dict__["_name_"] == "FLOOD"


def test_disaster_assessment_number_of_services_required(
    example_disaster: DisasterResponse,
):
    """Test the number of services required for a given disaster"""
    no_of_services_required = NearestServices.services_needed(example_disaster.dict())
    assert no_of_services_required == 2
    assert no_of_services_required != 3
    assert no_of_services_required != 5


def test_distribute_services(
    example_multiple_emergency_services: List[EmergencyServiceResponse],
):
    ...
