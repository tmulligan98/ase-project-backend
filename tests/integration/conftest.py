import pytest


@pytest.fixture
def example_user():
    """
    Test fixture for User
    """
    return {
        "user_id": "1234",
        "password": "letmein",
        "email": "admin@gmail.com",
        "name": "admin",
    }


@pytest.fixture
def example_disaster_report():
    """
    Test fixture for DisasterReport by civilians
    """
    return {"lat": 53, "long": 53, "scale": 3, "disaster_type": 2, "radius": 2}
