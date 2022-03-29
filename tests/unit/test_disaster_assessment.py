import pytest

from backend.database_wrapper.schemas import DisasterResponse
from backend.disaster_assessment.disaster_assesment import NearestServices
#from backend.emergency_services.models import EmergencyServiceModel


@pytest.fixture
def example_disaster():
    """
    Test fixture for DisasterResponse
        location : Trinity College Dublin
    """
    return DisasterResponse(
        id=0,
        disaster_type=2,
        scale=2,
        lat=53.34557035343706,
        long=-6.2564185279844065,
        radius=100,
        already_addressed=False,
        verified=False,
        completed=False,
    ).dict()


def test_disaster_assessment_number_of_services_required(
    example_disaster: DisasterResponse,
):
    """Test the number of services required for a given disaster"""
    no_of_services_required = NearestServices.services_needed(example_disaster)
    assert no_of_services_required == 2
    assert no_of_services_required != 3
    assert no_of_services_required != 5

