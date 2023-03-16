import unittest
from ships import read_filtered, get_co2_by_ship_type, get_fuel_by_ship_type, count_ship_types


class TestUtils(unittest.TestCase):

    # TODO: these tests rely on hard coded values from the database - is there a more robust way?
    def test_read_filtered(self):

        # Check querying by name
        res = read_filtered(ship_name='BOHUS')

        expected_name_result = [{'home_port': None, 'fuel_consumption_per_work_pax_laden': None,
                                 'verifier_city': '20457 Hamburg',
                                 'co2_emissions_between_ms_ports': 14623.63, 'through_ice': 0.0,
                                 'annual_avg_fuel_consumption_per_work_pax': 317.41, 'doc_expiry_date': '30/06/2020',
                                 'co2_emissions_per_work_dwt_laden': None, 'ice_class': 'IC',
                                 'total_co2_emissions': 16751.35,
                                 'co2_emissions_on_laden': None, 'port_of_registry': None,
                                 'verifier_country': 'Germany',
                                 'verifier_number': None, 'fuel_consumption_per_work_volume_laden': None,
                                 'fuel_consumption_per_work_dwt_laden': None, 'fuel_consumption_on_laden': None,
                                 'monitoring_method_b': None,
                                 'annual_avg_fuel_consumption_per_work_mass': None,
                                 'annual_avg_co2_emissions_per_work_freight': 206.78,
                                 'imo_number': 7037806, 'co2_emissions_arriving_ms_ports': 0.0,
                                 'monitoring_method_d': None,
                                 'doc_issue_date': '30/04/2019', 'monitoring_method_c': None,
                                 'verifier_address': 'Brooktorkai 18',
                                 'additional_info': None, 'annual_total_time_at_sea': 3753.82,
                                 'total_time_at_sea_ice': 0.0,
                                 'total_time_at_sea': 3753.82, 'co2_emissions_berthed_ms_ports': 2127.72,
                                 'annual_avg_co2_emissions_per_work_pax': 1017.63,
                                 'co2_emissions_per_work_pax_laden': None,
                                 'co2_emissions_freight': 2512.71, 'pk_ships': 5,
                                 'annual_avg_fuel_consumption_per_work_dwt': None,
                                 'fuel_consumption_per_work_mass_laden': None, 'co2_emissions_per_distance_laden': None,
                                 'co2_emissions_passenger': 14238.65, 'co2_emissions_per_work_volume_laden': None,
                                 'co2_emissions_per_work_freight_laden': None, 'reporting_period': 2018,
                                 'annual_avg_fuel_consumption_per_work_volume': None,
                                 'verifier_nab': 'German national accreditation body (DAkkS)',
                                 'annual_avg_co2_emissions_per_distance': 336.43,
                                 'verifier_accreditation_number': 'D-VS-16026-01-00', 'verifier_name': 'DNV GL',
                                 'annual_avg_fuel_consumption_per_distance': 104.94,
                                 'fuel_consumption_per_work_freight_laden': None,
                                 'total_fuel_consumption': 5225.0, 'fuel_consumption_per_distance_laden': None,
                                 'technical_efficiency': 'EIV (146 gCO₂/t·nm)', 'average_cargo_density': None,
                                 'ship_type': 'Ro-pax ship',
                                 'name': 'BOHUS', 'annual_avg_co2_emissions_per_work_volume': None,
                                 'monitoring_method_a': 'Yes',
                                 'annual_avg_fuel_consumption_per_work_freight': 64.5,
                                 'co2_emissions_departing_ms_ports': 0.0,
                                 'co2_emissions_per_work_mass_laden': None,
                                 'annual_avg_co2_emissions_per_work_mass': None,
                                 'annual_avg_co2_emissions_per_work_dwt': None}]

        self.assertEqual(res, expected_name_result)

        # Check querying by IMO
        res = read_filtered(ship_imo='5383304')
        expected_imo_result = [
            {'home_port': None, 'fuel_consumption_per_work_pax_laden': None, 'verifier_city': 'Piraeus',
             'co2_emissions_between_ms_ports': 16035.42, 'through_ice': None,
             'annual_avg_fuel_consumption_per_work_pax': 311.97, 'doc_expiry_date': '30/06/2020',
             'co2_emissions_per_work_dwt_laden': None, 'ice_class': None, 'total_co2_emissions': 20080.25,
             'co2_emissions_on_laden': None, 'port_of_registry': None, 'verifier_country': 'Greece',
             'verifier_number': None, 'fuel_consumption_per_work_volume_laden': None,
             'fuel_consumption_per_work_dwt_laden': None, 'fuel_consumption_on_laden': None,
             'monitoring_method_b': None, 'annual_avg_fuel_consumption_per_work_mass': None,
             'annual_avg_co2_emissions_per_work_freight': None, 'imo_number': 5383304,
             'co2_emissions_arriving_ms_ports': 974.78, 'monitoring_method_d': None, 'doc_issue_date': '05/02/2019',
             'monitoring_method_c': None, 'verifier_address': '16, Efplias Str.\n185 37 Piraeus, Greece',
             'additional_info': None, 'annual_total_time_at_sea': 4170.2, 'total_time_at_sea_ice': None,
             'total_time_at_sea': 4170.2, 'co2_emissions_berthed_ms_ports': 2341.47,
             'annual_avg_co2_emissions_per_work_pax': 993.14, 'co2_emissions_per_work_pax_laden': None,
             'co2_emissions_freight': None, 'pk_ships': 0, 'annual_avg_fuel_consumption_per_work_dwt': None,
             'fuel_consumption_per_work_mass_laden': None, 'co2_emissions_per_distance_laden': None,
             'co2_emissions_passenger': None, 'co2_emissions_per_work_volume_laden': None,
             'co2_emissions_per_work_freight_laden': None, 'reporting_period': 2018,
             'annual_avg_fuel_consumption_per_work_volume': None,
             'verifier_nab': 'Hellenic Accreditation System (ESYD)', 'annual_avg_co2_emissions_per_distance': 442.71,
             'verifier_accreditation_number': '1101', 'verifier_name': 'ICS Verification Services Single Member P.C.',
             'annual_avg_fuel_consumption_per_distance': 139.07, 'fuel_consumption_per_work_freight_laden': None,
             'total_fuel_consumption': 6307.75, 'fuel_consumption_per_distance_laden': None,
             'technical_efficiency': None, 'average_cargo_density': None, 'ship_type': 'Passenger ship',
             'name': 'ASTORIA', 'annual_avg_co2_emissions_per_work_volume': None, 'monitoring_method_a': 'Yes',
             'annual_avg_fuel_consumption_per_work_freight': None, 'co2_emissions_departing_ms_ports': 728.59,
             'co2_emissions_per_work_mass_laden': None, 'annual_avg_co2_emissions_per_work_mass': None,
             'annual_avg_co2_emissions_per_work_dwt': None},
            {'home_port': None, 'fuel_consumption_per_work_pax_laden': None, 'verifier_city': 'Piraeus',
             'co2_emissions_between_ms_ports': 17874.11, 'through_ice': None,
             'annual_avg_fuel_consumption_per_work_pax': 663.71, 'doc_expiry_date': '30/06/2021',
             'co2_emissions_per_work_dwt_laden': None, 'ice_class': None, 'total_co2_emissions': 24512.83,
             'co2_emissions_on_laden': None, 'port_of_registry': None, 'verifier_country': 'Greece',
             'verifier_number': None, 'fuel_consumption_per_work_volume_laden': None,
             'fuel_consumption_per_work_dwt_laden': None, 'fuel_consumption_on_laden': None,
             'monitoring_method_b': None, 'annual_avg_fuel_consumption_per_work_mass': None,
             'annual_avg_co2_emissions_per_work_freight': None, 'imo_number': 5383304,
             'co2_emissions_arriving_ms_ports': 695.02, 'monitoring_method_d': None, 'doc_issue_date': '15/03/2020',
             'monitoring_method_c': None, 'verifier_address': '16, Efplias Str.\n185 37 Piraeus, Greece',
             'additional_info': None, 'annual_total_time_at_sea': 4529.55, 'total_time_at_sea_ice': None,
             'total_time_at_sea': 4529.55, 'co2_emissions_berthed_ms_ports': 3693.58,
             'annual_avg_co2_emissions_per_work_pax': 2115.78, 'co2_emissions_per_work_pax_laden': None,
             'co2_emissions_freight': None, 'pk_ships': 12242, 'annual_avg_fuel_consumption_per_work_dwt': None,
             'fuel_consumption_per_work_mass_laden': None, 'co2_emissions_per_distance_laden': None,
             'co2_emissions_passenger': None, 'co2_emissions_per_work_volume_laden': None,
             'co2_emissions_per_work_freight_laden': None, 'reporting_period': 2019,
             'annual_avg_fuel_consumption_per_work_volume': None,
             'verifier_nab': 'Hellenic Accreditation System (ESYD)', 'annual_avg_co2_emissions_per_distance': 502.27,
             'verifier_accreditation_number': '1101', 'verifier_name': 'ICS Verification Services Single Member P.C.',
             'annual_avg_fuel_consumption_per_distance': 157.56, 'fuel_consumption_per_work_freight_laden': None,
             'total_fuel_consumption': 7689.55, 'fuel_consumption_per_distance_laden': None,
             'technical_efficiency': 'EIV (169.16 gCO₂/t·nm)', 'average_cargo_density': None,
             'ship_type': 'Passenger ship', 'name': 'ASTORIA', 'annual_avg_co2_emissions_per_work_volume': None,
             'monitoring_method_a': 'Yes', 'annual_avg_fuel_consumption_per_work_freight': None,
             'co2_emissions_departing_ms_ports': 2250.11, 'co2_emissions_per_work_mass_laden': None,
             'annual_avg_co2_emissions_per_work_mass': None, 'annual_avg_co2_emissions_per_work_dwt': None}]

        self.assertEqual(res, expected_imo_result)

        # Checking querying by name and IMO
        res = read_filtered(ship_name='ASTORIA', ship_imo='5383304')

        self.assertEqual(res, expected_imo_result)  # It's still the same result as just the IMO

        # Checking querying by name, IMO, and year
        res = read_filtered(ship_name='ASTORIA', ship_imo='5383304', year=2018)

        expected_name_imo_year_result = [
            {'co2_emissions_between_ms_ports': 16035.42, 'annual_avg_fuel_consumption_per_work_dwt': None,
             'annual_avg_co2_emissions_per_distance': 442.71, 'fuel_consumption_per_work_volume_laden': None,
             'ship_type': 'Passenger ship', 'annual_avg_fuel_consumption_per_distance': 139.07,
             'total_time_at_sea': 4170.2, 'port_of_registry': None, 'annual_total_time_at_sea': 4170.2,
             'technical_efficiency': None, 'fuel_consumption_per_work_pax_laden': None,
             'annual_avg_fuel_consumption_per_work_freight': None, 'co2_emissions_per_work_dwt_laden': None,
             'fuel_consumption_on_laden': None, 'fuel_consumption_per_work_dwt_laden': None,
             'co2_emissions_per_work_pax_laden': None, 'co2_emissions_freight': None, 'verifier_country': 'Greece',
             'additional_info': None, 'total_fuel_consumption': 6307.75, 'co2_emissions_arriving_ms_ports': 974.78,
             'fuel_consumption_per_distance_laden': None, 'fuel_consumption_per_work_mass_laden': None,
             'home_port': None, 'doc_issue_date': '05/02/2019', 'co2_emissions_per_work_freight_laden': None,
             'monitoring_method_b': None, 'verifier_city': 'Piraeus', 'total_co2_emissions': 20080.25,
             'reporting_period': 2018, 'co2_emissions_berthed_ms_ports': 2341.47, 'verifier_number': None,
             'verifier_address': '16, Efplias Str.\n185 37 Piraeus, Greece',
             'annual_avg_fuel_consumption_per_work_volume': None, 'co2_emissions_per_distance_laden': None,
             'through_ice': None, 'verifier_accreditation_number': '1101',
             'annual_avg_co2_emissions_per_work_pax': 993.14, 'fuel_consumption_per_work_freight_laden': None,
             'co2_emissions_per_work_mass_laden': None, 'annual_avg_co2_emissions_per_work_volume': None,
             'average_cargo_density': None, 'annual_avg_co2_emissions_per_work_dwt': None,
             'co2_emissions_departing_ms_ports': 728.59, 'verifier_nab': 'Hellenic Accreditation System (ESYD)',
             'co2_emissions_passenger': None, 'name': 'ASTORIA', 'annual_avg_co2_emissions_per_work_freight': None,
             'imo_number': 5383304, 'annual_avg_co2_emissions_per_work_mass': None, 'ice_class': None,
             'annual_avg_fuel_consumption_per_work_mass': None, 'co2_emissions_per_work_volume_laden': None,
             'doc_expiry_date': '30/06/2020', 'annual_avg_fuel_consumption_per_work_pax': 311.97,
             'monitoring_method_d': None, 'co2_emissions_on_laden': None,
             'verifier_name': 'ICS Verification Services Single Member P.C.', 'total_time_at_sea_ice': None,
             'pk_ships': 0, 'monitoring_method_c': None, 'monitoring_method_a': 'Yes'}]

        self.assertEqual(res, expected_name_imo_year_result)

        # Checking inconsistent/non-existent values
        res = read_filtered(ship_name='FLYING DUTCHMAN', ship_imo='666', year=2025)
        self.assertEqual(res, [])

    # TODO: finish these tests
    def test_get_co2_by_ship_type(self):
        pass

    def test_get_fuel_by_ship_type(self):
        pass

    def test_count_ship_types(self):
        pass