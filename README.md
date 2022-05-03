# README #

This is the repository for my Flask API accessing EU MRV data (https://mrv.emsa.europa.eu/#public/emission-report).

## Setup ##
### Downloading datasets ###
Download [EU MRV datasets](https://mrv.emsa.europa.eu/#public/emission-report) for 2018, 2019, and 2020 to the directory _api_hector/data_

The first time the API runs, it will create a SQLite database _mrv_emissions.db_ - this can take a few seconds, but only needs to happen once as subsequent API calls use this database.

### Dependencies ###
There are two options for running this API: either using docker, or traditional venv/conda-env.
Docker will be handy for just running the API as is, but unit tests will need venv/coda-env
#### Docker ####
A Dockerfile is provided with this repo. To use the API:
1. Create docker image `docker build --tag hector_api .` (note the vital full stop at the end of this command)
2. Run the image in detached mode with port forwarding `docker run -d -p 5000:5000 hector_api`
3. Navigate to [0.0.0.0:5000]() to interact with the API in your browser

#### Traditional ####
Both a _requirements.txt_ (venv or conda-env) and an _ENV.yml_ (conda-env) are provided. To use the API:
1. Create an environment using _requirements.txt_ or _ENV.yml_
2. Activate your environment
3. Within api_hector directory, `flask run`. This will start the flask API via the _.flaskenv_ file.

## Using this API ##
This API provides two endpoints, which can be accessed via your browser.
### Ships endpoint ###
[0.0.0.0:5000/ships]() returns all data from all ships across all years.
You can filter these results by any combination of:
- Ship Name with the argument 'name' e.g. [0.0.0.0:5000/ships?name=ASTORIA]()
- Ship IMO with the argument 'imo' e.g. [0.0.0.0:5000/ships?imo=5383304]()
- Year with the argument 'year' e.g. [0.0.0.0:5000/ships?year=2020]()

NOTE 1: If no year argument is specific, all matching data for 2018-2020 is returned
NOTE 2: Ships can share a name, so only IMO uniquely identifies a given vessel.

You can combine filters by separating them with an '&' symbol in the address, for example [0.0.0.0:5000/ships?name=ASTORIA&year=2020]()
### Total CO2 emissions endpoint ###
[0.0.0.0:5000/plots/totalCO2]() returns data on
- Proportion of total CO2 emissions for a given year per ship type
- Proportion of total ships each ship type represents

The intention is to help identify ship types that contribute more than their fair share of emissions.

Similarly to the ships endpoint, you can either filter by a specific year, or get all years by default. If all years are specified, an extra plot is created with data from all years combined.

### Browser choice ###
This API returns json objects, which are beautifully rendered in Firefox. I recommend this approach.

### Unit testing ###
Unit tests are provided in _hector_api/tests_

# To get in touch #
Any questions, comments, or enquiries welcome. 
Hector Page ([hpage90@gmail.com](mailto:hpage90@gmail.com))