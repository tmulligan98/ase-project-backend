import pytest
from backend.database_wrapper.schemas import DisasterResponse
from backend.emergency_services.models import (
    EmergencyServiceModel,
    EmergencyServiceResponse,
)
from .example_emergency_services import EXAMPLE_EMERGENCY_SERVICES


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
    )


@pytest.fixture
def example_single_emergency_service():
    """
    Test fixture for EmergencyServiceModel
        name : Fire Brigade
        type : Fire Brigade
    """
    return EmergencyServiceModel(
        name="Fire Brigade Service",
        type=1,
        lat=53.34848285683542,
        long=-6.260326800013764,
        units=14,
        units_available=10,
        units_busy=4,
    )


@pytest.fixture
def example_multiple_emergency_services():
    return list(
        map(
            lambda x: EmergencyServiceResponse(
                id=x["id"],
                name=x["name"],
                type=x["type"],
                lat=x["lat"],
                long=x["long"],
                units=x["units"],
                units_available=x["units_available"],
                units_busy=x["units_busy"],
            ),
            EXAMPLE_EMERGENCY_SERVICES,
        )
    )
