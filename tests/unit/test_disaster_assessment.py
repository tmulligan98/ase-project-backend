import unittest
from backend.disaster_assessment import get_nearest_services
from ..fixtures import EXAMPLE_DISASTERS, EXAMPLE_EMERGENCY_SERVICES


class TestDisasterAssessment(unittest.TestCase):
    def test_single_disaster_assessment(self):
        """
        Given some emergency service locations, assign the closest three to the disaster
        """

        res = get_nearest_services(
            disasters=[EXAMPLE_DISASTERS[0]],
            emergency_services=EXAMPLE_EMERGENCY_SERVICES,
        )

        print(res)
