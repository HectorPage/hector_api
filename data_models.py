from config import db, ma


class Ship(db.Model):
    __tablename__ = "ships"
    pk_ships = db.Column('PK_ships', db.Integer, primary_key=True, quote=True)
    imo_number = db.Column('IMO Number', db.Integer, quote=True)
    name = db.Column('Name', db.String, quote=True)
    ship_type = db.Column('Ship type', db.String, quote=True)
    reporting_period = db.Column('Reporting Period', db.Integer, quote=True)
    technical_efficiency = db.Column('Technical efficiency', db.String, quote=True)
    port_of_registry = db.Column('Port of Registry', db.String, quote=True)
    home_port = db.Column('Home Port', db.String, quote=True)
    ice_class = db.Column('Ice Class', db.String, quote=True)
    doc_issue_date = db.Column('DoC issue date', db.String, quote=True)  # TODO: use proper datetimes
    doc_expiry_date = db.Column('DoC expiry date', db.String, quote=True)
    verifier_number = db.Column('Verifier Number', db.String, quote=True)
    verifier_name = db.Column('Verifier Name', db.String, quote=True)
    verifier_nab = db.Column('Verifier NAB', db.String, quote=True)
    verifier_address = db.Column('Verifier Address', db.String, quote=True)
    verifier_city = db.Column('Verifier City', db.String, quote=True)
    verifier_accreditation_number = db.Column('Verifier Accreditation number', db.String, quote=True)
    verifier_country = db.Column('Verifier Country', db.String, quote=True)
    monitoring_method_a = db.Column('A', db.String, quote=True)
    monitoring_method_b = db.Column('B', db.String, quote=True)
    monitoring_method_c = db.Column('C', db.String, quote=True)
    monitoring_method_d = db.Column('D', db.String, quote=True)
    total_fuel_consumption = db.Column('Total fuel consumption [m tonnes]', db.Float, quote=True)
    fuel_consumption_on_laden = db.Column('Fuel consumptions assigned to On laden [m tonnes]', db.Float, quote=True)
    total_co2_emissions = db.Column('Total CO₂ emissions [m tonnes]', db.Float, quote=True)
    co2_emissions_between_ms_ports = db.Column('CO₂ emissions from all voyages between ports under a MS jurisdiction [m tonnes]', db.Float, quote=True)
    co2_emissions_departing_ms_ports= db.Column('CO₂ emissions from all voyages which departed from ports under a MS jurisdiction [m tonnes]', db.Float, quote=True)
    co2_emissions_arriving_ms_ports = db.Column('CO₂ emissions from all voyages to ports under a MS jurisdiction [m tonnes]', db.Float, quote=True)
    co2_emissions_berthed_ms_ports = db.Column('CO₂ emissions which occurred within ports under a MS jurisdiction at berth [m tonnes]', db.Float, quote=True)
    co2_emissions_passenger = db.Column('CO₂ emissions assigned to Passenger transport [m tonnes]', db.Float, quote=True)
    co2_emissions_freight = db.Column('CO₂ emissions assigned to Freight transport [m tonnes]', db.Float, quote=True)
    co2_emissions_on_laden = db.Column('CO₂ emissions assigned to On laden [m tonnes]', db.Float, quote=True)
    annual_total_time_at_sea = db.Column('Annual Total time spent at sea [hours]', db.Float, quote=True)
    annual_avg_fuel_consumption_per_distance = db.Column('Annual average Fuel consumption per distance [kg / n mile]', db.Float, quote=True)
    annual_avg_fuel_consumption_per_work_mass = db.Column('Annual average Fuel consumption per transport work (mass) [g / m tonnes · n miles]', db.Float, quote=True)
    annual_avg_fuel_consumption_per_work_volume = db.Column('Annual average Fuel consumption per transport work (volume) [g / m³ · n miles]', db.Float, quote=True)
    annual_avg_fuel_consumption_per_work_dwt = db.Column('Annual average Fuel consumption per transport work (dwt) [g / dwt carried · n miles]', db.Float, quote=True)
    annual_avg_fuel_consumption_per_work_pax = db.Column('Annual average Fuel consumption per transport work (pax) [g / pax · n miles]', db.Float, quote=True)
    annual_avg_fuel_consumption_per_work_freight = db.Column('Annual average Fuel consumption per transport work (freight) [g / m tonnes · n miles]', db.Float, quote=True)
    annual_avg_co2_emissions_per_distance = db.Column('Annual average CO₂ emissions per distance [kg CO₂ / n mile]', db.Float, quote=True)
    annual_avg_co2_emissions_per_work_mass = db.Column('Annual average CO₂ emissions per transport work (mass) [g CO₂ / m tonnes · n miles]', db.Float, quote=True)
    annual_avg_co2_emissions_per_work_volume = db.Column('Annual average CO₂ emissions per transport work (volume) [g CO₂ / m³ · n miles]', db.Float, quote=True)
    annual_avg_co2_emissions_per_work_dwt = db.Column('Annual average CO₂ emissions per transport work (dwt) [g CO₂ / dwt carried · n miles]', db.Float, quote=True)
    annual_avg_co2_emissions_per_work_pax = db.Column('Annual average CO₂ emissions per transport work (pax) [g CO₂ / pax · n miles]', db.Float, quote=True)
    annual_avg_co2_emissions_per_work_freight = db.Column('Annual average CO₂ emissions per transport work (freight) [g CO₂ / m tonnes · n miles]', db.Float, quote=True)
    through_ice = db.Column('Through ice [n miles]', db.Float, quote=True)
    total_time_at_sea = db.Column('Total time spent at sea [hours]', db.Float, quote=True)
    total_time_at_sea_ice = db.Column('Total time spent at sea through ice [hours]', db.Float, quote=True)
    fuel_consumption_per_distance_laden = db.Column('Fuel consumption per distance on laden voyages [kg / n mile]', db.Float, quote=True)
    fuel_consumption_per_work_mass_laden = db.Column('Fuel consumption per transport work (mass) on laden voyages [g / m tonnes · n miles]', db.Float, quote=True)
    fuel_consumption_per_work_volume_laden = db.Column('Fuel consumption per transport work (volume) on laden voyages [g / m³ · n miles]', db.Float, quote=True)
    fuel_consumption_per_work_dwt_laden = db.Column('Fuel consumption per transport work (dwt) on laden voyages [g / dwt carried · n miles]', db.Float, quote=True)
    fuel_consumption_per_work_pax_laden = db.Column('Fuel consumption per transport work (pax) on laden voyages [g / pax · n miles]', db.Float, quote=True)
    fuel_consumption_per_work_freight_laden = db.Column('Fuel consumption per transport work (freight) on laden voyages [g / m tonnes · n miles]', db.Float, quote=True)
    co2_emissions_per_distance_laden = db.Column('CO₂ emissions per distance on laden voyages [kg CO₂ / n mile]', db.Float, quote=True)
    co2_emissions_per_work_mass_laden = db.Column('CO₂ emissions per transport work (mass) on laden voyages [g CO₂ / m tonnes · n miles]', db.Float, quote=True)
    co2_emissions_per_work_volume_laden = db.Column('CO₂ emissions per transport work (volume) on laden voyages [g CO₂ / m³ · n miles]', db.Float, quote=True)
    co2_emissions_per_work_dwt_laden  = db.Column('CO₂ emissions per transport work (dwt) on laden voyages [g CO₂ / dwt carried · n miles]', db.Float, quote=True)
    co2_emissions_per_work_pax_laden = db.Column('CO₂ emissions per transport work (pax) on laden voyages [g CO₂ / pax · n miles]', db.Float, quote=True)
    co2_emissions_per_work_freight_laden = db.Column('CO₂ emissions per transport work (freight) on laden voyages [g CO₂ / m tonnes · n miles]', db.Float, quote=True)
    additional_info = db.Column('Additional information to facilitate the understanding of the reported average operational energy efficiency indicators', db.String, quote=True)
    average_cargo_density = db.Column('Average density of the cargo transported [m tonnes / m³]', db.Float, quote=True)


# https://realpython.com/flask-connexion-rest-api/
# https://realpython.com/flask-connexion-rest-api-part-2/


class ShipSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ship
        load_instance = True
        sqla_session = db.session


ship_schema = ShipSchema()
ships_schema = ShipSchema(many=True)
