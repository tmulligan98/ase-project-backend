import unittest
from fastapi.testclient import TestClient

# from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.database_wrapper import Base, get_db

# from backend.external_apis import get_tomtom_traffic_flow

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestExternalAPI(unittest.TestCase):

    # Example responses
    tomtom_example_response = {
        "frc": "FRC3",
        "currentSpeed": 63,
        "freeFlowSpeed": 63,
        "currentTravelTime": 152,
        "freeFlowTravelTime": 152,
        "confidence": 1,
        "roadClosure": False,
        "coordinates": {"coordinate": [{"latitude": 123.456, "longitude": 123.456}]},
        "@version": "blahblah",
    }

    """Suite of mock tests to ensure we can handle data from our chosen external APIs"""

    # @patch("backend.external_apis.external_apis.requests.get")
    # def test_tomtom_traffic_flow(self, mock_get):

    #     # Set up our sample response object
    #     d = {"flowSegmentData": self.tomtom_example_response}

    #     # Set up the called function to return this object
    #     instance = mock_get.return_value
    #     instance.content = json.dumps(d)

    #     # Run the call. This function should return a body of information regarding
    #     # ... traffic flow on nearby streets
    #     res = get_tomtom_traffic_flow(lat=123.456, long=123.456, zoom=18)

    #     # Assert that we are extracting information from the api response correctly
    #     self.assertEqual(res.streets[0].coords_of_street, [(123.456, 123.456)])
    #     self.assertEqual(res.streets[0].speed, 63)
