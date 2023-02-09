from flask import request, Response, render_template
from pandas_utils import read_given_years_to_df, clean_dataset
from utils import totals_to_percentages
from sql_utils import create_sqlite_database
from typing import Union
import os
import copy

import config
from ships import read_filtered, get_co2_by_ship_type, count_ship_types, get_fuel_by_ship_type
from plotting import create_scatter_plot, create_bar_plot


app = config.connex_app
app.add_api("swagger.yml")


# TODO: Pull the data from website directly?
# TODO: Use pandas instead of dicts where possible

# Do some setup if a database isn't already set up
if not os.path.exists('mrv_emissions.db'):
    print('...Loading MRV data into mrv_emissions.db...')
    # TODO: should unit test these as well
    # Set up an in-memory dict of pandas df per year (to avoid loading the data every request - openpyxl is really slow)
    ALL_YEARS_DATA = read_given_years_to_df(['2018', '2019', '2020'])
    ALL_YEARS_DATA = clean_dataset(ALL_YEARS_DATA)

    # Set up a sqlite database to demonstrate sql querying
    create_sqlite_database(ALL_YEARS_DATA)
else:
    print("Using existing mrv_emissions.db")


@app.route('/', methods=['GET'])
def home() -> str:
    return render_template("home.html")


@app.route("/ships", methods=['GET'])
def fetch_ships() -> Union[Response, str]:
    # Handle errors for invalid arguments
    invalid_args = []
    for arg in request.args:
        if arg not in {'name', 'imo', 'year'}:
            invalid_args.append(arg)
    if len(invalid_args) > 0:
        return f"Invalid arg(s) {invalid_args}.\nMust be one of [name, imo, year]"

    # TODO: implement filtering by ship/year/imo as part of the data table when returning all ships?
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
        year = int(request.args['year'])  # TODO: what about querying a pair of years?
        if year not in [2018, 2019, 2020]:
            return f"Invalid year {year}.\nMust be one of ['2018', '2019', '2020']"
    else:
        year = None

    # Read filtered ship data
    ships = read_filtered(ship_name, ship_imo, year)

    return render_template("tables.html", ships=ships)


@app.route('/plots/totalCO2', methods=['GET'])
def total_co2_emissions() -> Union[Response, str]:
    """
    Returns data grouped by ship type on:
    - Proportion of total CO2 emissions
    - Proportion of total vessels

     Returns data for year if specified, otherwise for all years.
     """
    # Handle errors for invalid arguments
    invalid_args = []
    for arg in request.args:
        if arg not in {'year'}:
            invalid_args.append(arg)
    if len(invalid_args) > 0:
        return f"Invalid arg(s) {invalid_args}.\nArgument must be either [year] or left blank."

    # Parse arguments
    if 'year' in request.args:
        year = request.args['year']
        if year not in ['2018', '2019', '2020']:
            return f"Invalid year {year}.\nMust be one of ['2018', '2019', '2020']"
    else:
        year = None  # Default to all years

    # Querying database to get necessary data
    co2_by_ship_type = get_co2_by_ship_type(year)
    ship_type_counts = count_ship_types(year)
    fuel_by_ship_type = get_fuel_by_ship_type(year)

    # Normalise data to show % of total in a given time period per ship
    proportion_co2_by_ship_type = totals_to_percentages(copy.deepcopy(co2_by_ship_type))
    proportion_ship_type_counts = totals_to_percentages(copy.deepcopy(ship_type_counts))
    proportion_fuel_by_ship_type = totals_to_percentages(copy.deepcopy(fuel_by_ship_type))

    # Create bar plot
    co2_by_ship_type_sorted = sorted(co2_by_ship_type.items(), key=lambda kv: -kv[1])
    co2_values = [item[1] for item in co2_by_ship_type_sorted]
    ship_values = [item[0] for item in co2_by_ship_type_sorted]
    graphJSON_co2 = create_bar_plot(co2_values, ship_values, co2_values,
                                    "Total CO₂ emissions [m tonnes]", "",  "")

    # Create scatter plots
    names = list(proportion_ship_type_counts.keys())
    ship_proportion_data = [proportion_ship_type_counts[key]
                            for key in proportion_ship_type_counts.keys()]
    emission_proportion_data = [proportion_co2_by_ship_type[key]
                                for key in proportion_ship_type_counts.keys()]
    fuel_proportion_data = [proportion_fuel_by_ship_type[key]
                            for key in proportion_fuel_by_ship_type.keys()]

    graphJSON_co2_ships = create_scatter_plot(ship_proportion_data, emission_proportion_data, names,
                                        "% of ships", "% of CO₂ emissions", "Ship Type")

    graphJSON_co2_fuel = create_scatter_plot(emission_proportion_data, fuel_proportion_data, names,
                                         "% of CO₂ emissions", "% of fuel consumption", "Ship Type")

    # Add in headers and descriptions
    if year is not None:
        header_co2 = f"Who emitted the most CO₂ in {year}?"
        header_co2_ships = f"Who emitted more than their fair share of CO₂ in {year}?"
        header_co2_fuel = "CO₂ emissions are determined by fuel consumption"
    else:
        header_co2 = "Who emitted the most CO₂ in 2018-2020?"
        header_co2_ships = "Who emitted more than their fair share of CO₂ in 2018-2020?"
        header_co2_fuel = "CO₂ emissions are determined by fuel consumption"

    description_co2 = f"""
            Container ships emitted the most CO₂ overall: {int(co2_by_ship_type['Container ship'])}
            metric tonnes.
           """

    description_co2_ships = f"""
        Container ships emitted much more CO₂ than would be expected given the proportion 
        of total ships in the EU MRV system that they 
        represent: ({proportion_co2_by_ship_type["Container ship"]:.2f}% of CO₂ 
        but just {proportion_ship_type_counts["Container ship"]:.2f}% of ships).
        On the other hand, Bulk Carriers emitted far less CO₂
        than expected given the proportion of ships they 
        represent ({proportion_co2_by_ship_type["Bulk carrier"]:.2f}% of CO₂
        , {proportion_ship_type_counts["Bulk carrier"]:.2f}% of ships).
       """

    description_co2_fuel = """
            The proportion of CO₂ emissions from a given ship type depends directly on fuel consumption for that
            ship type. Container ships emit more than their share of CO₂ because they burn more fuel per ship. 
            Similarly, Bulk Carriers burn less fuel per ship so emit less than their share of CO₂.
           """

    # TODO: this isn't very elegant usage of html template, could improve dashboard in the future
    return render_template('plots.html',
                           graphJSON1=graphJSON_co2, header1=header_co2, description1=description_co2,
                           graphJSON2=graphJSON_co2_ships, header2=header_co2_ships, description2=description_co2_ships,
                           graphJSON3=graphJSON_co2_fuel, header3=header_co2_fuel, description3=description_co2_fuel)


if __name__ == '__main__':
    app.run()
