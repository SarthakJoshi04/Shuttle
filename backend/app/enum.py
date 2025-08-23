import enum

class VehicleType(enum.Enum):
    CAR = "Car"
    BIKE = "Bike"

class EngineType(enum.Enum):
    PETROL = "Petrol"
    DIESEL = "Diesel"
    ELECTRIC = "Electric"
    HYBRID = "Hybrid"

class BodyType(enum.Enum):
    SEDAN = "Sedan"
    SUV = "SUV"
    HATCHBACK = "Hatchback"
    COUPE = "Coupe"
    CONVERTIBLE = "Convertible"
    CROSSOVER = "Crossover"
    PICKUP = "Pickup"
    VAN = "Van"
    # For bikes
    NAKED_SPORT = "Naked Sport"
    CRUISER = "Cruiser"
    SPORT = "Sport"
    TOURING = "Touring"
    ADVENTURE = "Adventure"
    DIRT = "Dirt"
    COMMUTER = "Commuter"
    SCOTTER = "Scooter"

class CarBodyType(enum.Enum):
    SEDAN = "Sedan"
    SUV = "SUV"
    HATCHBACK = "Hatchback"
    COUPE = "Coupe"
    CONVERTIBLE = "Convertible"
    CROSSOVER = "Crossover"
    PICKUP = "Pickup"
    VAN = "Van"

class BikeBodyType(enum.Enum):
    NAKED_SPORT = "Naked Sport"
    CRUISER = "Cruiser"
    SPORT = "Sport"
    TOURING = "Touring"
    ADVENTURE = "Adventure"
    DIRT = "Dirt"
    COMMUTER = "Commuter"
    SCOTTER = "Scooter"

class ListingType(enum.Enum):
    SALE = "Sale"
    RENTAL = "Rental"

class MajorCities(enum.Enum):
    BARDIYA = "Bardiya"
    BHAKTAPUR = "Bhaktapur"
    BHARATPUR = "Bharatpur"
    BIRATNAGAR = "Biratnagar"
    BIRGUNJ = "Birgunj"
    BUTWAL = "Butwal"
    CHITWAN = "Chitwan"
    DHANGADI = "Dhangadi"
    DHARAN = "Dharan"
    GORKHA = "Gorkha"
    HETAUDA = "Hetauda"
    ITAHARI = "Itahari"
    JANAKPUR = "Janakpur"
    KATHMANDU = "Kathmandu"
    LALITPUR = "Lalitpur"
    LUMBINI = "Lumbini"
    NEPALGUNJ = "Nepalgunj"
    POKHARA = "Pokhara"
