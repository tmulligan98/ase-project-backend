import unittest

import json
from unittest.mock import patch

from starlette.testclient import TestClient
from backend.main import app


class TestExternalAPIEndpoint(unittest.TestCase):

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

    def setUp(self):
        """Initialize the app"""
        self.test_app = TestClient(app)

    @patch("backend.external_apis.external_apis.requests.get")
    def test_tomtom_traffic_flow(self, mock_get):

        # Set up our sample response object
        d = {"flowSegmentData": self.tomtom_example_response}

        # Set up the called function to return this object
        instance = mock_get.return_value
        instance.content = json.dumps(d)

        # Run the call. This function should return a body of information regarding
        # ... traffic flow on nearby streets
        response = self.test_app.post(
            "/api/1/traffic_flow",
            data=json.dumps(
                {"lat": 12.34, "long": 12.34, "zoom": 10, "api_source": "tomtom"}
            ),
        )

        # Assert...
        self.assertEqual(response.status_code, 200)
        res = response.json()
        self.assertEqual(res["streets"][0]["speed"], 63)
