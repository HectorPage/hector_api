import pandas as pd
from openpyxl import load_workbook
from typing import Union, Dict
import os
import warnings


def read_given_years_to_df(years: Union[str, list]) -> Dict[str, pd.DataFrame]:
    """
    Function to load data for given years.
    """

    # Handling list or str input
    if isinstance(years, str):
        years = [years]

    datasets = {}
    for year in years:
        this_year_filename = find_data_for_year(year)
        datasets[year] = read_xlsx_to_df(this_year_filename)

    return datasets


def find_data_for_year(year: str) -> str:
    """
    Finds datasets for a given year.
    Assumes filename starts with year and ends with .xlsx
    """
    files_found = []
    data_dir = os.getcwd() + '/data'
    for file in os.listdir(data_dir):
        if file.startswith(year) and file.endswith('.xlsx'):
            files_found.append('data/'+file)

    num_files_found = len(files_found)

    if num_files_found == 1:  # should have a single .xlsx per year
        return files_found[0]
    elif num_files_found == 0:
        raise ValueError(f"No .xlsx files found for year {year}")
    else:
        raise ValueError(f"Too many .xlsx files ({num_files_found}) found for year {year}. "
                         f"One file per year required.")


def read_xlsx_to_df(filename: str) -> pd.DataFrame:
    """
    Reads xlsx file to pandas dataframe.
    Note: Assumes data is in the first/only sheet
    """
    # Loading a workbook whilst suppressing openpyxl warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = load_workbook(filename)

    df = pd.DataFrame(wb[wb.sheetnames[0]].values)

    # Set df columns as third header row
    df.columns = df.iloc[2].values

    # First two header rows not needed
    df = df.iloc[3:]

    return df
