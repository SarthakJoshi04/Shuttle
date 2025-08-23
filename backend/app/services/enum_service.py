from app.enum import MajorCities
from app.enum import VehicleType
from app.enum import EngineType
from app.enum import CarBodyType
from app.enum import BikeBodyType
from app.enum import ListingType

def get_all_cities():
    return [city.value for city in MajorCities]

def get_all_vehicle_types():
    return [vehicle_type.value for vehicle_type in VehicleType]

def get_all_engine_types():
    return [engine_type.value for engine_type in EngineType]

def get_car_body_types():
    return [car_body_type.value for car_body_type in CarBodyType]

def get_bike_body_types():
    return [bike_body_type.value for bike_body_type in BikeBodyType]

def get_all_listing_types():
    return [listing_type.value for listing_type in ListingType]