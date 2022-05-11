import sys
import unittest
from utils import sum_groupby_results_across_years, totals_to_percentages


sys.path.append('../')

# TODO: convert to pytest


class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.numbers_by_ship_type = {'2018': {'A': 1, 'B': 5, 'C': 2, 'D': 8},
                                    '2019': {'B': 8, 'C': 11, 'D': 1},
                                    '2020': {'A': 9, 'B': 2, 'C': 6}}

    def test_sum_groupby_results_across_years(self) -> None:
        result = sum_groupby_results_across_years(self.numbers_by_ship_type)
        self.assertDictEqual(result, {'B': 15, 'C': 19})

    def test_totals_to_percentages(self) -> None:
        result = totals_to_percentages(self.numbers_by_ship_type)
        self.assertDictEqual(result, {'2018': {'A': 1/16, 'B': 5/16, 'C': 2/16, 'D': 8/16},
                                      '2019': {'B': 8/20, 'C': 11/20, 'D': 1/20},
                                      '2020': {'A': 9/17, 'B': 2/17, 'C': 6/17}})



