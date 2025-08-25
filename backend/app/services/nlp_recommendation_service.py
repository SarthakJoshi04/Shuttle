import logging
from typing import List, Optional
from dataclasses import dataclass
from sqlalchemy.orm import Session

# Project-specific models and schemas
from app.models.vehicle_listing import VehicleListing
from app.models.vehicle import Vehicle
from app.models.user import User
from app.schemas.vehicle_listing import VehicleListingOut
from app.enum import VehicleType, BodyType, EngineType, MajorCities

# --------------------------
# Logger configuration
# --------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ExtractedPreferences:
    """
    Stores extracted vehicle preferences from a user query.
    """
    vehicle_type: Optional[VehicleType] = None
    body_types: Optional[List[BodyType]] = None
    engine_type: Optional[EngineType] = None
    purposes: Optional[List[str]] = None
    confidence_score: float = 0.0


class NLPRecommendationService:
    """
    Service for extracting user preferences from queries and generating vehicle listing recommendations.
    """
    def __init__(self):
        self.vehicle_knowledge = self._build_knowledge_base()

    def _build_knowledge_base(self) -> dict:
        """
        Build a simple keyword knowledge base for vehicles, body types, engines, and purposes.

        Returns:
            dict: Knowledge base mapping categories to keywords.
        """
        return {
            "vehicle_types": {
                VehicleType.CAR: {"keywords": ["car", "automobile", "sedan", "suv", "hatchback", "coupe", "crossover", "pickup", "van"]},
                VehicleType.BIKE: {"keywords": ["bike", "motorcycle", "scooter", "yamaha", "honda", "ducati", "kawasaki"]}
            },
            "body_types": {
                BodyType.SUV: {"keywords": ["suv", "sport utility", "spacious", "off-road", "family", "seven seater"]},
                BodyType.SEDAN: {"keywords": ["sedan", "saloon", "four door", "comfortable", "executive"]},
                BodyType.HATCHBACK: {"keywords": ["hatchback", "compact", "small", "city car", "economical"]},
                BodyType.COUPE: {"keywords": ["coupe", "sporty", "two door", "sports", "fast"]},
                BodyType.CONVERTIBLE: {"keywords": ["convertible", "cabriolet", "open top", "roadster"]},
                BodyType.PICKUP: {"keywords": ["pickup", "truck", "utility", "cargo", "load"]},
                BodyType.CROSSOVER: {"keywords": ["crossover", "cuv", "compact suv", "versatile"]},
                BodyType.VAN: {"keywords": ["van", "minivan", "people carrier", "mpv", "group"]},
                BodyType.NAKED_SPORT: {"keywords": ["naked sport", "naked", "sport bike"]},
                BodyType.CRUISER: {"keywords": ["cruiser", "harley", "classic"]},
                BodyType.SPORT: {"keywords": ["sport", "racing", "performance", "supersport"]},
                BodyType.TOURING: {"keywords": ["touring", "long distance", "comfortable"]},
                BodyType.ADVENTURE: {"keywords": ["adventure", "off-road", "dual-sport", "enduro"]},
                BodyType.DIRT: {"keywords": ["dirt", "motocross", "off-road"]},
                BodyType.COMMUTER: {"keywords": ["commuter", "daily ride", "economical"]},
                BodyType.SCOTTER: {"keywords": ["scooter", "scooty", "vespa"]}
            },
            "engine_types": {
                EngineType.ELECTRIC: {"keywords": ["electric", "ev", "battery", "eco", "tesla"]},
                EngineType.HYBRID: {"keywords": ["hybrid", "fuel efficient", "economical", "prius"]},
                EngineType.PETROL: {"keywords": ["petrol", "gasoline", "gas", "unleaded"]},
                EngineType.DIESEL: {"keywords": ["diesel", "torque", "highway"]}
            },
            "purposes": {
                "family": {"keywords": ["family", "kids", "children", "safe", "spacious"]},
                "city": {"keywords": ["city", "urban", "commute", "parking", "traffic"]},
                "tour": {"keywords": ["tour", "travel", "trip", "vacation", "journey"]},
                "adventure": {"keywords": ["adventure", "off-road", "camping", "mountain"]},
                "business": {"keywords": ["business", "professional", "work", "office", "corporate"]},
                "sport": {"keywords": ["sport", "racing", "fast", "performance"]}
            }
        }

    def extract_preferences(self, query: str) -> ExtractedPreferences:
        """
        Extract vehicle preferences from a user query string.

        Args:
            query (str): User input query.

        Returns:
            ExtractedPreferences: Structured preference data with confidence score.
        """
        q = query.lower()
        preferences = ExtractedPreferences(confidence_score=70)

        # Vehicle type
        for vt, data in self.vehicle_knowledge["vehicle_types"].items():
            if any(k in q for k in data["keywords"]):
                preferences.vehicle_type = vt
                break

        # Body types
        body_types = [
            bt for bt, data in self.vehicle_knowledge["body_types"].items() if any(k in q for k in data["keywords"])
        ]
        preferences.body_types = body_types if body_types else None

        # Engine type
        for et, data in self.vehicle_knowledge["engine_types"].items():
            if any(k in q for k in data["keywords"]):
                preferences.engine_type = et
                break

        # Purposes
        purposes = [
            purpose for purpose, data in self.vehicle_knowledge["purposes"].items() if any(k in q for k in data["keywords"])
        ]
        preferences.purposes = purposes if purposes else None

        return preferences

    def calculate_match_score(self, listing: VehicleListingOut, preferences: ExtractedPreferences) -> float:
        """
        Calculate a match score between a listing and extracted preferences.

        Args:
            listing (VehicleListingOut): Vehicle listing output schema.
            preferences (ExtractedPreferences): User preferences.

        Returns:
            float: Match score (0-100).
        """
        score = 0
        if preferences.vehicle_type and listing.vehicle.vehicle_type == preferences.vehicle_type:
            score += 30
        if preferences.body_types and listing.vehicle.body_type in preferences.body_types:
            score += 20
        if preferences.engine_type and listing.vehicle.engine_type == preferences.engine_type:
            score += 15
        return min(score, 100)

    def get_recommendations(self, db: Session, query: str, location: str = None, limit: int = 10) -> dict:
        """
        Generate a list of recommended vehicle listings based on a query and optional location.

        Args:
            db (Session): Database session.
            query (str): User query.
            location (str, optional): City filter. Defaults to None.
            limit (int, optional): Max number of results. Defaults to 10.

        Returns:
            dict: Recommendations and query analysis.
        """
        preferences = self.extract_preferences(query)

        db_query = db.query(VehicleListing).join(Vehicle).join(User)

        if location:
            try:
                location_enum = MajorCities(location)
                db_query = db_query.filter(VehicleListing.location == location_enum)
            except ValueError:
                logger.warning(f"Invalid location provided: {location}")

        listings = db_query.all()

        recs = []
        for l in listings:
            l_out = VehicleListingOut.model_validate(l)
            score = self.calculate_match_score(l_out, preferences)
            if score > 20:
                listing_dict = l_out.model_dump()
                listing_dict["user"] = {
                    "id": l.user.id,
                    "fullname": l.user.fullname,
                    "phone_number": l.user.phone_number
                }
                recs.append({
                    "listing": listing_dict,
                    "match_score": score,
                    "match_reasons": ["Matches your preferences"],
                    "confidence": preferences.confidence_score
                })

        recs.sort(key=lambda x: x["match_score"], reverse=True)

        return {
            "recommendations": recs[:limit],
            "query_analysis": f"Processed '{query}'" + (f" for location '{location}'" if location else ""),
            "extracted_preferences": {
                "vehicle_type": preferences.vehicle_type.value if preferences.vehicle_type else None,
                "body_types": [bt.value for bt in preferences.body_types] if preferences.body_types else None,
                "engine_type": preferences.engine_type.value if preferences.engine_type else None,
                "purposes": preferences.purposes,
                "confidence_score": preferences.confidence_score
            }
        }


# --------------------------
# Global service instance
# --------------------------
nlp_service = NLPRecommendationService()