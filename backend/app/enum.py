import enum

class VehicleType(enum.Enum):
    """Types of vehicles."""
    CAR = "Car"
    BIKE = "Bike"


class EngineType(enum.Enum):
    """Types of engines available for vehicles."""
    PETROL = "Petrol"
    DIESEL = "Diesel"
    ELECTRIC = "Electric"
    HYBRID = "Hybrid"


class BodyType(enum.Enum):
    """All body types for cars and bikes combined."""
    # Car types
    SEDAN = "Sedan"
    SUV = "SUV"
    HATCHBACK = "Hatchback"
    COUPE = "Coupe"
    CONVERTIBLE = "Convertible"
    CROSSOVER = "Crossover"
    PICKUP = "Pickup"
    VAN = "Van"
    
    # Bike types
    NAKED_SPORT = "Naked Sport"
    CRUISER = "Cruiser"
    SPORT = "Sport"
    TOURING = "Touring"
    ADVENTURE = "Adventure"
    DIRT = "Dirt"
    COMMUTER = "Commuter"
    SCOTTER = "Scooter"


class CarBodyType(enum.Enum):
    """Body types specific to cars."""
    SEDAN = "Sedan"
    SUV = "SUV"
    HATCHBACK = "Hatchback"
    COUPE = "Coupe"
    CONVERTIBLE = "Convertible"
    CROSSOVER = "Crossover"
    PICKUP = "Pickup"
    VAN = "Van"


class BikeBodyType(enum.Enum):
    """Body types specific to bikes."""
    NAKED_SPORT = "Naked Sport"
    CRUISER = "Cruiser"
    SPORT = "Sport"
    TOURING = "Touring"
    ADVENTURE = "Adventure"
    DIRT = "Dirt"
    COMMUTER = "Commuter"
    SCOTTER = "Scooter"


class ListingType(enum.Enum):
    """Types of vehicle listings."""
    SALE = "Sale"
    RENTAL = "Rental"


class MajorCities(enum.Enum):
    """Supported major cities for vehicle listings."""
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