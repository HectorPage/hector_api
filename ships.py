from flask import abort


from data_models import Ship, ships_schema
from typing import Union, ByteString, Dict
from sqlalchemy import func
from config import db


def read_filtered(ship_name: Union[str, None], ship_imo: Union[str, None], year: Union[str, None]) -> ByteString:

    # Handling different combinations of ship name and ship IMO
    if ship_name is not None and ship_imo is not None:
        if year is not None:
            ships = Ship.query.filter_by(name=ship_name).filter_by(imo_number=ship_imo).filter_by(reporting_period=year)

        else:
            ships = Ship.query.filter_by(name=ship_name).filter_by(imo_number=ship_imo)

    elif ship_name is not None:
        if year is not None:
            ships = Ship.query.filter_by(name=ship_name).filter_by(reporting_period=year)

        else:
            ships = Ship.query.filter_by(name=ship_name)

    elif ship_imo is not None:
        if year is not None:
            ships = Ship.query.filter_by(imo_number=ship_imo).filter_by(reporting_period=year)

        else:
            ships = Ship.query.filter_by(imo_number=ship_imo)

    else:
        if year is not None:
            ships = Ship.query.filter_by(reporting_period=year)

        else:
            ships = Ship.query.all()

    if ships is not None:
        return ships_schema.dump(ships)
    else:
        abort(404, f"Data not found")


def get_co2_by_ship_type(year: Union[str, None]) -> Dict:

    if year is not None:
        response = db.session.query(Ship.ship_type, func.sum(Ship.total_co2_emissions))\
            .filter(Ship.reporting_period == int(year)).group_by(Ship.ship_type).all()
    else:
        response = db.session.query(Ship.ship_type, func.sum(Ship.total_co2_emissions)).group_by(Ship.ship_type).all()

    return {response_tuple[0]: response_tuple[1] for response_tuple in response}


def count_ship_types(year: Union[str, None]) -> Dict:

    if year is not None:
        response = db.session.query(Ship.ship_type, func.count(Ship.ship_type))\
            .filter(Ship.reporting_period == int(year)).group_by(Ship.ship_type).all()
    else:
        response = db.session.query(Ship.ship_type, func.count(Ship.ship_type)).group_by(Ship.ship_type).all()

    return {response_tuple[0]: response_tuple[1] for response_tuple in response}


