from flask import Flask, request, jsonify, Response, render_template
from pandas_utils import read_given_years_to_df, clean_dataset
from utils import totals_to_percentages, clean_response
from sql_utils import create_sqlite_database
from typing import Union
import os
import copy
import json
import plotly
import plotly.express as px
import math

import config
from ships import read_filtered, get_co2_by_ship_type, count_ship_types


app = config.connex_app
app.add_api("swagger.yml")


# TODO: Pull the data from website directly?
# TODO: Use SQLAlchemy ORM for database management, access, etc.
# TODO: Use pandas instead of dicts where possible

# Do some setup if a database isn't already set up
if not os.path.exists('mrv_emissions.db'):
    print('...Loading MRV data into mrv_emissions.db...')
    # TODO: should unit test these as well, but ran out of time
    # Set up an in-memory dict of pandas df per year (to avoid loading the data every request - openpyxl is really slow)
    ALL_YEARS_DATA = read_given_years_to_df(['2018', '2019', '2020'])
    ALL_YEARS_DATA = clean_dataset(ALL_YEARS_DATA)

    # Set up a sqlite database to demonstrate sql querying
    create_sqlite_database(ALL_YEARS_DATA)
else:
    print("Using existing mrv_emissions.db")


@app.route('/', methods=['GET'])
def home() -> str:
    # TODO: could use proper HTML rendering with a template:
    #  https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates
    return "This is Hector Page's API for EU MRV data on CO2 emissions from maritime transport 2018-20." \
           "<br/>See here for more details: https://mrv.emsa.europa.eu/#public/emission-report" \
           "<br/>For enquiries/questions contact: hpage90@gmail.com"


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

    # Normalise data to show % of total in a given time period per ship
    proportion_co2_by_ship_type = totals_to_percentages(copy.deepcopy(co2_by_ship_type))
    proportion_ship_type_counts = totals_to_percentages(copy.deepcopy(ship_type_counts))

    # TODO: create a navigation page like this for multiple types of plot:
    #  https://towardsdatascience.com/web-visualization-with-plotly-and-flask-3660abf9c946
    # Create plot
    # TODO: make this plotting a separate function perhaps?
    ship_proportion_data = [proportion_ship_type_counts[key]
                            for key in proportion_ship_type_counts.keys()]
    emission_proportion_data = [proportion_co2_by_ship_type[key]
                                for key in proportion_ship_type_counts.keys()]
    names = list(proportion_ship_type_counts.keys())
    fig = px.scatter(x=ship_proportion_data,
                     y=emission_proportion_data,
                     color=names,
                     labels={
                         "x": "% of ships",
                         "y": "% of CO₂ emissions",
                         "color": "Ship Type"
                     }
                     )
    fig.update_traces(mode="markers")
    # Set axis limits
    max_x = max(ship_proportion_data)
    max_y = max(emission_proportion_data)

    overall_max = math.ceil(max([max_x, max_y]))
    fig.update_layout(xaxis=dict(range=[0, overall_max]))
    fig.update_layout(yaxis=dict(range=[0, overall_max]))
    fig.add_shape(type="line",
                  x0=0,
                  y0=0,
                  x1=overall_max,
                  y1=overall_max,
                  layer='below',
                  opacity=0.5)

    # Export plot
    if year is not None:
        header = f"Who emitted the most CO₂ in {year}?"
    else:
        header = "Who emitted the most CO₂ in 2018-2020?"

    description = """
        Container ships emitted the greatest proportion of CO₂ - much more than would be expected given the proportion 
        of total ships in the EU MRV system that they represent.
       """

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('plots.html', graphJSON=graphJSON, header=header, description=description)


if __name__ == '__main__':
    app.run()
