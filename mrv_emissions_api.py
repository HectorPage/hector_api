from flask import Flask, request, jsonify, Response
from pandas_utils import read_given_years_to_df
from utils import sum_groupby_results_across_years, totals_to_percentages, clean_response
from sql_utils import create_sqlite_database, query_db_with_args, get_co2_by_ship_type, count_ship_types
from typing import Union
import os
import copy
app = Flask(__name__)


# TODO: Pull the data from website directly?
# Do some setup if a database isn't already set up
if not os.path.exists('mrv_emissions.db'):
    print('...Loading MRV data into mrv_emissions.db...')
    # TODO: should unit test these as well, but ran out of time
    # Set up an in-memory dict of pandas df per year (to avoid loading the data every request - openpyxl is really slow)
    ALL_YEARS_DATA = read_given_years_to_df(['2018', '2019', '2020'])

    # Set up a sqlite database to demonstrate sql querying
    create_sqlite_database(ALL_YEARS_DATA)


@app.route('/', methods=['GET'])
def home() -> str:
    # TODO: could use proper HTML rendering with a template:
    #  https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates
    return "This is Hector Page's API for EU MRV data on CO2 emissions from maritime transport 2018-20." \
           "<br/>See here for more details: https://mrv.emsa.europa.eu/#public/emission-report" \
           "<br/>For enquiries/questions contact: hpage90@gmail.com"


@app.route('/ships', methods=['GET'])
def fetch_ships() -> Union[Response, str]:
    """
     Method to return ship records, with the option of specifying any combination of:
     - Year (all years if not specified)
     - Ship name
     - Ship IMO

     If neither name or IMO are specified, all ships will be returned for chosen year(s).

     NOTE: Ships can share a name, so only IMOs uniquely identify a vessel.
     """

    # Some simple error handling
    invalid_args = []
    for arg in request.args:
        if arg not in {'name', 'imo', 'year'}:
            invalid_args.append(arg)
    if len(invalid_args) > 0:
        return f"Invalid arg(s) {invalid_args}.\nMust be one of [name, imo, year]"

    # Parse arguments
    if 'name' in request.args:  # TODO: what about multiple names/IMOs?
        ship_name = request.args['name'].upper()  # Accept lower case ship names
    else:
        ship_name = None

    if 'imo' in request.args:
        ship_imo = request.args['imo']
    else:
        ship_imo = None

    if 'year' in request.args:
        years = [request.args['year']]  # TODO: what about querying a pair of years?
    else:
        years = ['2018', '2019', '2020']  # Default to all years

    # Filter data based on ship name/IMO and years
    filtered_data = query_db_with_args(ship_name, ship_imo, years)

    # Clean  up the response by adding in field names and grouping them
    for year in filtered_data.keys():
        if len(filtered_data[year]) > 0:  # Invalid name/imo combinations return empty lists
            filtered_data[year] = clean_response(filtered_data[year])

    return jsonify(filtered_data)


@app.route('/plots/totalCO2', methods=['GET'])
def total_co2_emissions() -> Union[Response, str]:
    """
    Returns data grouped by ship type on:
    - Proportion of total CO2 emissions
    - Proportion of total vessels

     Returns data for year if specified, otherwise for all years.
     """
    # Some simple error handling
    invalid_args = []
    for arg in request.args:
        if arg not in {'year'}:
            invalid_args.append(arg)
    if len(invalid_args) > 0:
        return f"Invalid arg(s) {invalid_args}.\nArgument must be either [year] or left blank."

    if 'year' in request.args:
        years = [request.args['year']]
    else:
        years = ['2018', '2019', '2020']  # Default to all years

    # Querying database to get necessary data
    co2_by_ship_type = {}
    ship_type_counts = {}
    for year in years:
        co2_by_ship_type[year] = get_co2_by_ship_type(year)
        ship_type_counts[year] = count_ship_types(year)

    # If we've queried > 1 years, add in total across years
    if len(years) > 1:
        year_keys = list(co2_by_ship_type.keys())
        year_keys.sort(key=int)
        co2_by_ship_type[year_keys[0]+'-'+year_keys[-1]] = sum_groupby_results_across_years(co2_by_ship_type)
        ship_type_counts[year_keys[0]+'-'+year_keys[-1]] = sum_groupby_results_across_years(ship_type_counts)

    # Normalise data to show % of total in a given time period per ship
    proportion_co2_by_ship_type = totals_to_percentages(copy.deepcopy(co2_by_ship_type))
    proportion_ship_type_counts = totals_to_percentages(copy.deepcopy(ship_type_counts))

    # TODO: I wanted a plot of these but ran out of time (flask/matplotlib interaction is new to me and quite fiddly)
    # Group results per year
    co2_and_count_per_ship_type = {year_key: {'co2 emissions': {'value': co2_by_ship_type[year_key],
                                                                'proportion': proportion_co2_by_ship_type[year_key]},
                                              'number of ships': {'value': ship_type_counts[year_key],
                                                                  'proportion': proportion_ship_type_counts[year_key]}}
                                   for year_key in co2_by_ship_type.keys()}

    return jsonify(co2_and_count_per_ship_type)


if __name__ == '__main__':
    app.run()
