import unittest
from unittest.mock import patch, MagicMock


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

    @patch("backend.utils.utils.get_traffic_flow")
    def test_tomtom_traffic_flow(self, mock_resource):

        mock_flow = MagicMock()
        # Set up our sample response object
        d = {"flowSegmentData": self.tomtom_example_response}
        mock_flow.__getitem__.side_effect = d.__getitem__

        # Set up the called function to return this object
        mock_resource.return_value = mock_flow

        # Run the call. This function should return a body of information regarding
        # ... traffic flow on nearby streets
        # res = get_tomtom_traffic_flow(lat=123.456, long=123.456)

        # Assert that we are extracting information from the api response correctly
        self.assertEqual()
