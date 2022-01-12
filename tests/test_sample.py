import unittest


class TestSamples(unittest.TestCase):
    def test_sum(self):
        assert sum([1, 2, 3]) == 6
