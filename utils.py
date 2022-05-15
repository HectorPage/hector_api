from typing import List, Tuple, Dict, Union


def original_dataset_fields() -> List:
    return [
        'IMO Number', 'Name', 'Ship type', 'Reporting Period',
        'Technical efficiency', 'Port of Registry', 'Home Port', 'Ice Class',
        'DoC issue date', 'DoC expiry date', 'Verifier Number', 'Verifier Name',
        'Verifier NAB', 'Verifier Address', 'Verifier City',
        'Verifier Accreditation number', 'Verifier Country', 'A', 'B', 'C', 'D',
        'Total fuel consumption [m tonnes]',
        'Fuel consumptions assigned to On laden [m tonnes]',
        'Total CO₂ emissions [m tonnes]',
        'CO₂ emissions from all voyages between ports under a MS jurisdiction [m tonnes]',
        'CO₂ emissions from all voyages which departed from ports under a MS jurisdiction [m tonnes]',
        'CO₂ emissions from all voyages to ports under a MS jurisdiction [m tonnes]',
        'CO₂ emissions which occurred within ports under a MS jurisdiction at berth [m tonnes]',
        'CO₂ emissions assigned to Passenger transport [m tonnes]',
        'CO₂ emissions assigned to Freight transport [m tonnes]',
        'CO₂ emissions assigned to On laden [m tonnes]',
        'Annual Total time spent at sea [hours]',
        'Annual average Fuel consumption per distance [kg / n mile]',
        'Annual average Fuel consumption per transport work (mass) [g / m tonnes · n miles]',
        'Annual average Fuel consumption per transport work (volume) [g / m³ · n miles]',
        'Annual average Fuel consumption per transport work (dwt) [g / dwt carried · n miles]',
        'Annual average Fuel consumption per transport work (pax) [g / pax · n miles]',
        'Annual average Fuel consumption per transport work (freight) [g / m tonnes · n miles]',
        'Annual average CO₂ emissions per distance [kg CO₂ / n mile]',
        'Annual average CO₂ emissions per transport work (mass) [g CO₂ / m tonnes · n miles]',
        'Annual average CO₂ emissions per transport work (volume) [g CO₂ / m³ · n miles]',
        'Annual average CO₂ emissions per transport work (dwt) [g CO₂ / dwt carried · n miles]',
        'Annual average CO₂ emissions per transport work (pax) [g CO₂ / pax · n miles]',
        'Annual average CO₂ emissions per transport work (freight) [g CO₂ / m tonnes · n miles]',
        'Through ice [n miles]', 'Total time spent at sea [hours]',
        'Total time spent at sea through ice [hours]',
        'Fuel consumption per distance on laden voyages [kg / n mile]',
        'Fuel consumption per transport work (mass) on laden voyages [g / m tonnes · n miles]',
        'Fuel consumption per transport work (volume) on laden voyages [g / m³ · n miles]',
        'Fuel consumption per transport work (dwt) on laden voyages [g / dwt carried · n miles]',
        'Fuel consumption per transport work (pax) on laden voyages [g / pax · n miles]',
        'Fuel consumption per transport work (freight) on laden voyages [g / m tonnes · n miles]',
        'CO₂ emissions per distance on laden voyages [kg CO₂ / n mile]',
        'CO₂ emissions per transport work (mass) on laden voyages [g CO₂ / m tonnes · n miles]',
        'CO₂ emissions per transport work (volume) on laden voyages [g CO₂ / m³ · n miles]',
        'CO₂ emissions per transport work (dwt) on laden voyages [g CO₂ / dwt carried · n miles]',
        'CO₂ emissions per transport work (pax) on laden voyages [g CO₂ / pax · n miles]',
        'CO₂ emissions per transport work (freight) on laden voyages [g CO₂ / m tonnes · n miles]',
        'Additional information to facilitate the understanding of the reported average operational energy efficiency indicators',
        'Average density of the cargo transported [m tonnes / m³]']


def clean_response(sql_query_response: List[Tuple]) -> Dict[str, Dict]:
    """Takes a sql query response for ships matching certain filters, adds field names, and groups fields"""
    cleaned_response = {}
    for ship_found in sql_query_response:
        response_with_names = {field_name: query_response_val for field_name, query_response_val
                               in zip(original_dataset_fields(), ship_found)}

        grouped_response = group_metrics(response_with_names)
        cleaned_response[response_with_names['IMO Number']] = grouped_response

    # TODO: produce a simpler/shorter set of column names
    # TODO: add info to the response (e.g. descriptions from xlsx file or units)
    # TODO: clean up the fields e.g. replace missing values replace null with N/A?
    return cleaned_response


def group_metrics(ship_data: Dict) -> Dict:
    """Groups ship data in the same manner as original xlsx datasets"""
    grouped_ship_data = {
        "Ship": {'IMO Number': ship_data['IMO Number'],
                 'Name': ship_data['Name'],
                 'Ship type': ship_data['Ship type'],
                 'Reporting Period': ship_data['Reporting Period'],
                 'Technical efficiency': ship_data['Technical efficiency'],
                 'Port of Registry': ship_data['Port of Registry'],
                 'Home Port': ship_data['Home Port'],
                 'Ice Class': ship_data['Ice Class']
                 },
        "DOC": {'DoC issue date': ship_data['DoC issue date'],
                'DoC expiry date': ship_data['DoC expiry date']
                },
        "Verifier": {'Verifier Number': ship_data['Verifier Number'],
                     'Verifier Name': ship_data['Verifier Name'],
                     'Verifier NAB': ship_data['Verifier NAB'],
                     'Verifier Address': ship_data['Verifier Address'],
                     'Verifier City': ship_data['Verifier City'],
                     'Verifier Accreditation number': ship_data['Verifier Accreditation number'],
                     'Verifier Country': ship_data['Verifier Country'],
                     },
        "Monitoring Methods": {
            "A": ship_data["A"],
            "B": ship_data["B"],
            "C": ship_data["C"],
            "D": ship_data["D"],
        },
        "Annual Monitoring Results": {
            "Totals": {
                'Total fuel consumption [m tonnes]': ship_data['Total fuel consumption [m tonnes]'],
                'Fuel consumptions assigned to On laden [m tonnes]': ship_data[
                    'Fuel consumptions assigned to On laden [m tonnes]'],
                'Total CO₂ emissions [m tonnes]': ship_data['Total CO₂ emissions [m tonnes]'],
                'CO₂ emissions from all voyages between ports under a MS jurisdiction [m tonnes]': ship_data[
                    'CO₂ emissions from all voyages between ports under a MS jurisdiction [m tonnes]'],
                'CO₂ emissions from all voyages which departed from ports under a MS jurisdiction [m tonnes]':
                    ship_data[
                        'CO₂ emissions from all voyages which departed from ports under a MS jurisdiction [m tonnes]'],
                'CO₂ emissions from all voyages to ports under a MS jurisdiction [m tonnes]': ship_data[
                    'CO₂ emissions from all voyages to ports under a MS jurisdiction [m tonnes]'],
                'CO₂ emissions which occurred within ports under a MS jurisdiction at berth [m tonnes]': ship_data[
                    'CO₂ emissions which occurred within ports under a MS jurisdiction at berth [m tonnes]'],
                'CO₂ emissions assigned to Passenger transport [m tonnes]': ship_data[
                    'CO₂ emissions assigned to Passenger transport [m tonnes]'],
                'CO₂ emissions assigned to Freight transport [m tonnes]': ship_data[
                    'CO₂ emissions assigned to Freight transport [m tonnes]'],
                'CO₂ emissions assigned to On laden [m tonnes]': ship_data[
                    'CO₂ emissions assigned to On laden [m tonnes]'],
                'Annual Total time spent at sea [hours]': ship_data['Annual Total time spent at sea [hours]'],

            },
            "Average Energy Efficiency": {
                'Annual average Fuel consumption per distance [kg / n mile]': ship_data[
                    'Annual average Fuel consumption per distance [kg / n mile]'],
                'Annual average Fuel consumption per transport work (mass) [g / m tonnes · n miles]': ship_data[
                    'Annual average Fuel consumption per transport work (mass) [g / m tonnes · n miles]'],
                'Annual average Fuel consumption per transport work (volume) [g / m³ · n miles]': ship_data[
                    'Annual average Fuel consumption per transport work (volume) [g / m³ · n miles]'],
                'Annual average Fuel consumption per transport work (dwt) [g / dwt carried · n miles]': ship_data[
                    'Annual average Fuel consumption per transport work (dwt) [g / dwt carried · n miles]'],
                'Annual average Fuel consumption per transport work (pax) [g / pax · n miles]': ship_data[
                    'Annual average Fuel consumption per transport work (pax) [g / pax · n miles]'],
                'Annual average Fuel consumption per transport work (freight) [g / m tonnes · n miles]': ship_data[
                    'Annual average Fuel consumption per transport work (freight) [g / m tonnes · n miles]'],
                'Annual average CO₂ emissions per distance [kg CO₂ / n mile]': ship_data[
                    'Annual average CO₂ emissions per distance [kg CO₂ / n mile]'],
                'Annual average CO₂ emissions per transport work (mass) [g CO₂ / m tonnes · n miles]': ship_data[
                    'Annual average CO₂ emissions per transport work (mass) [g CO₂ / m tonnes · n miles]'],
                'Annual average CO₂ emissions per transport work (volume) [g CO₂ / m³ · n miles]': ship_data[
                    'Annual average CO₂ emissions per transport work (volume) [g CO₂ / m³ · n miles]'],
                'Annual average CO₂ emissions per transport work (dwt) [g CO₂ / dwt carried · n miles]': ship_data[
                    'Annual average CO₂ emissions per transport work (dwt) [g CO₂ / dwt carried · n miles]'],
                'Annual average CO₂ emissions per transport work (pax) [g CO₂ / pax · n miles]': ship_data[
                    'Annual average CO₂ emissions per transport work (pax) [g CO₂ / pax · n miles]'],
                'Annual average CO₂ emissions per transport work (freight) [g CO₂ / m tonnes · n miles]': ship_data[
                    'Annual average CO₂ emissions per transport work (freight) [g CO₂ / m tonnes · n miles]'],

            },
        },
        "Voluntary Reporting": {
            "Distance and Time": {'Through ice [n miles]': ship_data['Through ice [n miles]'],
                                  'Total time spent at sea [hours]': ship_data['Total time spent at sea [hours]'],
                                  'Total time spent at sea through ice [hours]': ship_data[
                                      'Total time spent at sea through ice [hours]']
                                  },
            "Average energy efficiency on Laden Voyages": {
                'Fuel consumption per distance on laden voyages [kg / n mile]': ship_data[
                    'Fuel consumption per distance on laden voyages [kg / n mile]'],
                'Fuel consumption per transport work (mass) on laden voyages [g / m tonnes · n miles]': ship_data[
                    'Fuel consumption per transport work (mass) on laden voyages [g / m tonnes · n miles]'],
                'Fuel consumption per transport work (volume) on laden voyages [g / m³ · n miles]': ship_data[
                    'Fuel consumption per transport work (volume) on laden voyages [g / m³ · n miles]'],
                'Fuel consumption per transport work (dwt) on laden voyages [g / dwt carried · n miles]': ship_data[
                    'Fuel consumption per transport work (dwt) on laden voyages [g / dwt carried · n miles]'],
                'Fuel consumption per transport work (pax) on laden voyages [g / pax · n miles]': ship_data[
                    'Fuel consumption per transport work (pax) on laden voyages [g / pax · n miles]'],
                'Fuel consumption per transport work (freight) on laden voyages [g / m tonnes · n miles]': ship_data[
                    'Fuel consumption per transport work (freight) on laden voyages [g / m tonnes · n miles]'],
                'CO₂ emissions per distance on laden voyages [kg CO₂ / n mile]': ship_data[
                    'CO₂ emissions per distance on laden voyages [kg CO₂ / n mile]'],
                'CO₂ emissions per transport work (mass) on laden voyages [g CO₂ / m tonnes · n miles]': ship_data[
                    'CO₂ emissions per transport work (mass) on laden voyages [g CO₂ / m tonnes · n miles]'],
                'CO₂ emissions per transport work (volume) on laden voyages [g CO₂ / m³ · n miles]': ship_data[
                    'CO₂ emissions per transport work (volume) on laden voyages [g CO₂ / m³ · n miles]'],
                'CO₂ emissions per transport work (dwt) on laden voyages [g CO₂ / dwt carried · n miles]': ship_data[
                    'CO₂ emissions per transport work (dwt) on laden voyages [g CO₂ / dwt carried · n miles]'],
                'CO₂ emissions per transport work (pax) on laden voyages [g CO₂ / pax · n miles]': ship_data[
                    'CO₂ emissions per transport work (pax) on laden voyages [g CO₂ / pax · n miles]'],
                'CO₂ emissions per transport work (freight) on laden voyages [g CO₂ / m tonnes · n miles]': ship_data[
                    'CO₂ emissions per transport work (freight) on laden voyages [g CO₂ / m tonnes · n miles]']}
        },
        "Additional Voluntary Reporting": {
            'Additional information to facilitate the understanding of the reported average operational energy efficiency indicators':
                ship_data[
                    'Additional information to facilitate the understanding of the reported average operational energy efficiency indicators'],
            'Average density of the cargo transported [m tonnes / m³]': ship_data[
                'Average density of the cargo transported [m tonnes / m³]']}
    }

    return grouped_ship_data


def totals_to_percentages(input_data: Dict[str, Union[float, int]]) -> Dict[str, Dict]:
    """Converts a dict of numbers into percentages"""
    total = sum(input_data.values())
    return {key: (value/total)*100 for key, value in input_data.items()}
