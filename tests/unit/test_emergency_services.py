from backend.emergency_services.models import ServiceType, EmergencyServiceModel


def test_emergency_service_type(
    example_single_emergency_service: EmergencyServiceModel,
):
    """Test the type of emergency service"""
    assert example_single_emergency_service.type == ServiceType.FIRE_BRIGADE
    assert not example_single_emergency_service.type == ServiceType.AMBULANCE
    assert not example_single_emergency_service.type == ServiceType.GARDA
