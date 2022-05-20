import sys
import unittest
import sqlite3
import os
import pandas as pd
from sql_utils import get_co2_by_ship_type, count_ship_types, query_db_with_args


sys.path.append('../')

# TODO: switch to pytest


class TestSqlUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # Building test SQLite database
        conn = sqlite3.connect('test.db')
        cur = conn.cursor()

        # Create tables
        create_table = 'CREATE TABLE ships("IMO Number" PRIMARY KEY, Name, ' \
                       '"Ship type", "Reporting Period", "Total CO₂ emissions [m tonnes]")'
        cur.execute(create_table)
        conn.commit()

        # Populate these tables
        values_list = [('1', 'A', 'Type_1', '2018', 5),
                       ('2', 'B', 'Type_1', '2018', 1),
                       ('3', 'C', 'Type_2', '2018', 13),
                       ('4', 'A', 'Type_1', '2019', 11),
                       ('5', 'B', 'Type_2', '2019', 2),
                       ('6', 'C', 'Type_2', '2019', 4),
                       ('7', 'A', 'Type_1', '2020', 12),
                       ('8', 'A', 'Type_1', '2020', 5),
                       ('9', 'B', 'Type_2', '2020', 6),
                       ('10', 'B', 'Type_2', '2020', 10)]

        for values in values_list:
            add_rec_syntax = 'INSERT INTO ships ("IMO NUMBER", Name, "Ship type", "Reporting Period",' \
                             ' "Total CO₂ emissions [m tonnes]") VALUES {}'.format(values)
            cur.execute(add_rec_syntax)
            conn.commit()

        conn.close()

        cls.columns = ["IMO Number", "Name", "Ship type", "Reporting Period", "Total CO₂ emissions [m tonnes]"]

    def test_query_db_with_args(self) -> None:

        # Name defined in query
        response = query_db_with_args('A', None, None, 'test.db')
        self.assertTrue(response.equals(pd.DataFrame(data=[('1', 'A', 'Type_1', '2018', 5),
                                                      ('4', 'A', 'Type_1', '2019', 11),
                                                      ('7', 'A', 'Type_1', '2020', 12),
                                                      ('8', 'A', 'Type_1', '2020', 5)],
                                                     columns=self.columns)))

        # No name or imo
        response = query_db_with_args(None, None, '2020', 'test.db')
        self.assertTrue(response.equals(pd.DataFrame(data=[('7', 'A', 'Type_1', '2020', 12),
                                                      ('8', 'A', 'Type_1', '2020', 5),
                                                      ('9', 'B', 'Type_2', '2020', 6),
                                                      ('10', 'B', 'Type_2', '2020', 10)],
                                                     columns=self.columns)))
        # Name and imo
        response = query_db_with_args('A', '4', '2019', 'test.db')
        self.assertTrue(response.equals(pd.DataFrame(data=[('4', 'A', 'Type_1', '2019', 11)],
                                                     columns=self.columns)))

        # No name but imo
        response = query_db_with_args(None, '3', None, 'test.db')
        self.assertTrue(response.equals(pd.DataFrame(data=[('3', 'C', 'Type_2', '2018', 13)],
                                                     columns=self.columns)))

        # Incompatible name and imo
        response = query_db_with_args('A', '3', None, 'test.db')
        self.assertTrue(response.equals(pd.DataFrame(data=[],
                                                     columns=self.columns)))

    def test_get_co2_by_ship_type(self) -> None:
        result = get_co2_by_ship_type('2018', 'test.db')
        self.assertDictEqual(result, {'Type_1': 6, 'Type_2': 13})

        result = get_co2_by_ship_type('2019', 'test.db')
        self.assertDictEqual(result, {'Type_1': 11, 'Type_2': 6})

        result = get_co2_by_ship_type('2020', 'test.db')
        self.assertDictEqual(result, {'Type_1': 17, 'Type_2': 16})

    def test_count_ship_types(self) -> None:
        result = count_ship_types('2018', 'test.db')
        self.assertDictEqual(result, {'Type_1': 2, 'Type_2': 1})

        result = count_ship_types('2019', 'test.db')
        self.assertDictEqual(result, {'Type_1': 1, 'Type_2': 2})

        result = count_ship_types('2020', 'test.db')
        self.assertDictEqual(result, {'Type_1': 2, 'Type_2': 2})

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove('test.db')


