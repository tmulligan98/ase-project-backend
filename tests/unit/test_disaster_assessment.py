from backend.database_wrapper.schemas import DisasterResponse
from backend.disaster_assessment.disaster_assesment import NearestServices
from typing import Dict, List


def test_disaster_type(example_disaster: DisasterResponse):
    """Test the type of disaster"""
    assert example_disaster.disaster_type.__dict__["_name_"] == "ROAD_INCIDENT"
    assert not example_disaster.disaster_type.__dict__["_name_"] == "FLOOD"


def test_disaster_assessment_number_of_services_required(
    example_disaster: DisasterResponse,
):
    """Test the number of services required for a given disaster"""
    no_of_services_required = NearestServices.services_needed(example_disaster.dict())
    assert no_of_services_required == (2, 0)
    assert no_of_services_required != (3, 0)
    assert no_of_services_required != (5, 0)


def test_distribute_services(
    example_multiple_emergency_services: List[Dict],
):
    distributed_emergency_services = NearestServices.distribute_services(
        example_multiple_emergency_services
    )
    assert len(distributed_emergency_services) == 4
    assert len(distributed_emergency_services["fire_brigade"]) == 1
    assert len(distributed_emergency_services["garda"]) == 3
    assert len(distributed_emergency_services["ambulance"]) == 4
    assert not len(distributed_emergency_services["fire_brigade"]) == 2
    assert distributed_emergency_services["ambulance"][1]["name"] == "cineworld"


def test_n_nearest_services(
    example_disaster: DisasterResponse,
    example_distributed_emergency_services: List[Dict],
):

    (
        first_nearest_services,
        second_nearest_services,
        third_nearest_services,
    ) = NearestServices.n_nearest_services(
        example_disaster.dict(), example_distributed_emergency_services
    )
    assert first_nearest_services is not None
    assert second_nearest_services is not None
    assert third_nearest_services is not None


def test_n_nearest_services_with_transport(
    example_disaster_high_scale: DisasterResponse,
    example_distributed_transport_services: List[Dict],
):

    (
        first_nearest_services,
        second_nearest_services,
        third_nearest_services,
    ) = NearestServices.n_nearest_ts_services(
        example_disaster_high_scale.dict(), example_distributed_transport_services
    )

    assert list(first_nearest_services.keys())[0] == "DepotC"
    assert list(second_nearest_services.keys())[0] == "DepotA"
    assert list(third_nearest_services.keys())[0] == "DepotB"
