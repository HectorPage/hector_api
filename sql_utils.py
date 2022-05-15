import pandas as pd
from typing import Dict, List, Union
import sqlite3
from utils import original_dataset_fields


def create_sqlite_database(years_data: Dict[str, pd.DataFrame]) -> None:
    """"Create SQLite database loaded with MRV emissions data"""
    db_name = 'mrv_emissions.db'
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Add the table
    cols = original_dataset_fields()
    create_table_syntax = f'CREATE TABLE ships("{cols[0]}" PRIMARY KEY, "{cols[1]}", "{cols[2]}", "{cols[3]}",' \
                          f' "{cols[4]}", "{cols[5]}", "{cols[6]}", "{cols[7]}", "{cols[8]}", "{cols[9]}", "{cols[10]}",' \
                          f' "{cols[11]}", "{cols[12]}","{cols[13]}", "{cols[14]}", "{cols[15]}", "{cols[16]}",' \
                          f' "{cols[17]}", "{cols[18]}", "{cols[19]}", "{cols[20]}", "{cols[21]}", "{cols[22]}",' \
                          f' "{cols[23]}", "{cols[24]}", "{cols[25]}", "{cols[26]}", "{cols[27]}", "{cols[28]}",' \
                          f' "{cols[29]}", "{cols[30]}", "{cols[31]}", "{cols[32]}", "{cols[33]}", "{cols[34]}",' \
                          f' "{cols[35]}", "{cols[36]}", "{cols[37]}", "{cols[38]}", "{cols[39]}", "{cols[40]}",' \
                          f' "{cols[41]}", "{cols[42]}", "{cols[43]}", "{cols[44]}", "{cols[45]}", "{cols[46]}",' \
                          f' "{cols[47]}", "{cols[48]}", "{cols[49]}", "{cols[50]}", "{cols[51]}", "{cols[52]}",' \
                          f' "{cols[53]}", "{cols[54]}", "{cols[55]}", "{cols[56]}", "{cols[57]}", "{cols[58]}",' \
                          f' "{cols[59]}", "{cols[60]}")'

    c.execute(create_table_syntax)
    conn.commit()

    # Go through each year and add/append to the ships table
    for year, year_df in years_data.items():
        # Handling 2020 column naming differences (some names changed vs 2018 and 2019)
        if year == '2020':
            year_df = year_df.rename(columns={'Annual Time spent at sea [hours]': 'Annual Total time spent at sea [hours]',
                                              'Time spent at sea [hours]': 'Total time spent at sea [hours]'})
        year_df.to_sql(name='ships', con=conn, if_exists='append', index=False)
    conn.close()


# TODO: could be a more informative name here - if we have other functions this might not be the only query type
def query_db_with_args(ship_name: Union[str, None], ship_imo: Union[str, None],
                       year: Union[str, None], db_name: str = 'mrv_emissions.db') -> List:
    """Queries database for ship data that matches the filter arguments for name/imo/year"""
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    # TODO: error handling if wrong database specified etc.

    # Handling different combinations of ship name and ship IMO
    if ship_name is not None and ship_imo is not None:
        if year is not None:
            query_string = f"SELECT * FROM ships WHERE Name=? AND [IMO Number]=? AND [Reporting Period]=?;"
            response = cur.execute(query_string, (ship_name, ship_imo, year)).fetchall()

        else:
            query_string = f"SELECT * FROM ships WHERE Name=? AND [IMO Number]=?;"
            response = cur.execute(query_string, (ship_name, ship_imo)).fetchall()

    elif ship_name is not None:
        if year is not None:
            query_string = f"SELECT * FROM ships WHERE Name=? AND [Reporting Period]=?;"
            response = cur.execute(query_string, (ship_name, year)).fetchall()
        else:
            query_string = f"SELECT * FROM ships WHERE Name=?;"
            response = cur.execute(query_string, (ship_name, year)).fetchall()

    elif ship_imo is not None:
        if year is not None:
            query_string = f"SELECT * FROM ships WHERE [IMO Number]=? AND [Reporting Period]=?;"
            response = cur.execute(query_string, (ship_imo, year)).fetchall()
        else:
            query_string = f"SELECT * FROM ships WHERE [IMO Number]=?;"
            response = cur.execute(query_string, (ship_imo,)).fetchall()
    else:
        query_string = f"SELECT * FROM ships;"
        response = cur.execute(query_string).fetchall()

    conn.close()

    return response


def get_co2_by_ship_type(year: str, db_name: str = 'mrv_emissions.db') -> Dict:
    """Queries database for total CO2 emissions grouped by ship type"""
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    year_string = 'ships_'+year
    query_string = f'SELECT SUM("Total CO₂ emissions [m tonnes]"), "Ship type" FROM {year_string}' \
                   f' GROUP BY "Ship type" ORDER BY SUM("Total CO₂ emissions [m tonnes]");'

    response = cur.execute(query_string).fetchall()

    conn.close()

    return {response_tuple[1]: response_tuple[0] for response_tuple in response}


def count_ship_types(year: str, db_name: str = 'mrv_emissions.db') -> Dict:
    """Queries database for total number of ships of each type"""
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    year_string = 'ships_'+year
    query_string = f'SELECT COUNT("Ship type"), "Ship type" FROM {year_string} GROUP BY "Ship type";'

    response = cur.execute(query_string).fetchall()

    conn.close()

    return {response_tuple[1]: response_tuple[0] for response_tuple in response}
