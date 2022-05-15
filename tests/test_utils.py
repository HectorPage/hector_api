import sys
import unittest
from utils import totals_to_percentages


sys.path.append('../')

# TODO: convert to pytest


class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.numbers_by_ship_type = {'A': 1, 'B': 5, 'C': 2, 'D': 8}

    def test_totals_to_percentages(self) -> None:
        result = totals_to_percentages(self.numbers_by_ship_type)
        self.assertDictEqual(result, {'A': (1/16)*100, 'B': (5/16)*100, 'C': (2/16)*100, 'D': (8/16)*100})



