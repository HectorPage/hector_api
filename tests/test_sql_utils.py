import sys
import unittest
import sqlite3
import os
from sql_utils import get_co2_by_ship_type, count_ship_types, query_db_with_args


sys.path.append('../')

# TODO: convert to pytest


class TestSqlUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # Building test SQLite database
        conn = sqlite3.connect('test.db')
        cur = conn.cursor()

        # Create tables
        create_table = 'CREATE TABLE ships_2018("IMO Number" PRIMARY KEY, Name, ' \
                 '"Ship type", "Total CO₂ emissions [m tonnes]")'
        cur.execute(create_table)
        conn.commit()

        create_table = 'CREATE TABLE ships_2019("IMO Number" PRIMARY KEY, Name, ' \
                       '"Ship type", "Total CO₂ emissions [m tonnes]")'
        cur.execute(create_table)
        conn.commit()

        create_table = 'CREATE TABLE ships_2020("IMO Number" PRIMARY KEY, Name, ' \
                       '"Ship type", "Total CO₂ emissions [m tonnes]")'
        cur.execute(create_table)
        conn.commit()

        # Populate these tables
        values_2018 = [('1', 'A', 'Type_1', 5),
                       ('2', 'B', 'Type_1', 1),
                       ('3', 'C', 'Type_2', 13)]

        values_2019 = [('1', 'A', 'Type_1', 11),
                       ('2', 'B', 'Type_2', 2),
                       ('3', 'C', 'Type_2', 4)]

        values_2020 = [('1', 'A', 'Type_1', 12),
                       ('2', 'A', 'Type_1', 5),
                       ('3', 'B', 'Type_2', 6),
                       ('4', 'B', 'Type_2', 10)]

        for values in values_2018:
            add_rec_syntax = 'INSERT INTO ships_2018 ("IMO NUMBER", Name, "Ship type",' \
                             ' "Total CO₂ emissions [m tonnes]") VALUES {}'.format(values)
            cur.execute(add_rec_syntax)
            conn.commit()

        for values in values_2019:
            add_rec_syntax = 'INSERT INTO ships_2019 ("IMO NUMBER", Name, "Ship type",' \
                             ' "Total CO₂ emissions [m tonnes]") VALUES {}'.format(values)
            cur.execute(add_rec_syntax)
            conn.commit()

        for values in values_2020:
            add_rec_syntax = 'INSERT INTO ships_2020 ("IMO NUMBER", Name, "Ship type",' \
                             ' "Total CO₂ emissions [m tonnes]") VALUES {}'.format(values)
            cur.execute(add_rec_syntax)
            conn.commit()

        conn.close()

    def test_query_db_with_args(self) -> None:

        # Name defined in query
        response = query_db_with_args('A', None, ['2018', '2019', '2020'], 'test.db')
        self.assertEqual(response, {'2018': [('1', 'A', 'Type_1', 5)],
                                    '2019': [('1', 'A', 'Type_1', 11)],
                                    '2020': [('1', 'A', 'Type_1', 12), ('2', 'A', 'Type_1', 5)]})

        # No name or imo
        response = query_db_with_args(None, None, ['2020'], 'test.db')
        self.assertEqual(response, {'2020': [('1', 'A', 'Type_1', 12),
                                             ('2', 'A', 'Type_1', 5),
                                             ('3', 'B', 'Type_2', 6),
                                             ('4', 'B', 'Type_2', 10)]})
        # Name and imo
        response = query_db_with_args('A', '1', ['2019'], 'test.db')
        self.assertEqual(response, {'2019': [('1', 'A', 'Type_1', 11)]})

        # No name but imo
        response = query_db_with_args(None, '3', ['2018', '2019', '2020'], 'test.db')
        self.assertEqual(response, {'2018': [('3', 'C', 'Type_2', 13)],
                                    '2019': [('3', 'C', 'Type_2', 4)],
                                    '2020': [('3', 'B', 'Type_2', 6)]})

        # Incompatible name and imo
        response = query_db_with_args('A', '3', ['2018', '2019', '2020'], 'test.db')
        self.assertEqual(response, {'2018': [],
                                    '2019': [],
                                    '2020': []})

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


