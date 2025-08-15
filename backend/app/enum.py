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
    # For cars
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

class ListingType(enum.Enum):
    SALE = "Sale"
    RENTAL = "Rental"

class MajorCities(enum.Enum):
    KATHMANDU = "Kathmandu"
    LALITPUR = "Lalitpur"
    BHAKTAPUR = "Bhaktapur"
    POKHARA = "Pokhara"
    CHITWAN = "Chitwan"
    BIRATNAGAR = "Biratnagar"
    HETAUDA = "Hetauda"
    BUTWAL = "Butwal"
    DHARAN = "Dharan"
    BIRGUNJ = "Birgunj"
    JANAKPUR = "Janakpur"
    ITAHARI = "Itahari"
    NEPALGUNJ = "Nepalgunj"
    DHANGADI = "Dhangadi"
    BHARATPUR = "Bharatpur"
    LUMBINI = "Lumbini"
    BARDIYA = "Bardiya"
    GORKHA = "Gorkha"