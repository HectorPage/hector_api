import pandas as pd
import sqlite3
from utils import original_dataset_fields


def create_sqlite_database(df: pd.DataFrame) -> None:
    """"Create SQLite database loaded with MRV emissions data"""
    db_name = 'mrv_emissions.db'
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Add the table
    cols = original_dataset_fields()
    create_table_syntax = f'CREATE TABLE ships(PK_ships PRIMARY KEY, "{cols[0]}", "{cols[1]}", "{cols[2]}", "{cols[3]}",' \
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

    # Writing to database
    df.to_sql(name='ships', con=conn, if_exists='append', index=True, index_label='PK_ships')
    conn.close()

