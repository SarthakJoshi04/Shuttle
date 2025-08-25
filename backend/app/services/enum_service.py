# Enums
from app.enum import (
    MajorCities,
    VehicleType,
    EngineType,
    CarBodyType,
    BikeBodyType,
    ListingType
)

def get_all_cities() -> list[str]:
    """Return a list of all city names (MajorCities enum values)."""
    return [city.value for city in MajorCities]


def get_all_vehicle_types() -> list[str]:
    """Return a list of all vehicle types (VehicleType enum values)."""
    return [vehicle_type.value for vehicle_type in VehicleType]


def get_all_engine_types() -> list[str]:
    """Return a list of all engine types (EngineType enum values)."""
    return [engine_type.value for engine_type in EngineType]


def get_car_body_types() -> list[str]:
    """Return a list of all car body types (CarBodyType enum values)."""
    return [car_body_type.value for car_body_type in CarBodyType]


def get_bike_body_types() -> list[str]:
    """Return a list of all bike body types (BikeBodyType enum values)."""
    return [bike_body_type.value for bike_body_type in BikeBodyType]


def get_all_listing_types() -> list[str]:
    """Return a list of all listing types (ListingType enum values)."""
    return [listing_type.value for listing_type in ListingType]