from backend.app.enum import MajorCities

def get_all_cities():
    return [city.value for city in MajorCities]