import pandas as pd
import sqlite3
from utils import original_dataset_fields


def create_sqlite_database(df: pd.DataFrame) -> None:
    """"Create SQLite database loaded with MRV emissions data"""
    db_name = 'mrv_emissions.db'
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Get original columns
    cols = original_dataset_fields()

    # Building SQL syntax for creating table with necessary cols
    create_table_syntax = f'CREATE TABLE ships(PK_ships PRIMARY KEY'
    for col_num in range(0, len(cols)):
        create_table_syntax += f', "{cols[col_num]}"'
    create_table_syntax += ')'

    # Add the table
    c.execute(create_table_syntax)
    conn.commit()

    # Writing to database
    df.to_sql(name='ships', con=conn, if_exists='append', index=True, index_label='PK_ships')
    conn.close()

