# app/services/nlp_recommendation_service.py
import logging
from typing import List, Optional
from dataclasses import dataclass
from sqlalchemy.orm import Session

from app.models.vehicle_listing import VehicleListing
from app.models.vehicle import Vehicle
from app.schemas.vehicle_listing import VehicleListingOut
from app.enum import VehicleType, BodyType, EngineType
from app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ExtractedPreferences:
    vehicle_type: Optional[VehicleType] = None
    body_types: Optional[List[BodyType]] = None
    engine_type: Optional[EngineType] = None
    purposes: Optional[List[str]] = None
    confidence_score: float = 0.0

class NLPRecommendationService:
    def __init__(self):
        # Build a simple keyword knowledge base
        self.vehicle_knowledge = self._build_knowledge_base()

    def _build_knowledge_base(self):
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
        q = query.lower()
        preferences = ExtractedPreferences(confidence_score=70)

        # Vehicle type
        for vt, data in self.vehicle_knowledge["vehicle_types"].items():
            if any(k in q for k in data["keywords"]):
                preferences.vehicle_type = vt
                break

        # Body type
        body_types = []
        for bt, data in self.vehicle_knowledge["body_types"].items():
            if any(k in q for k in data["keywords"]):
                body_types.append(bt)
        preferences.body_types = body_types if body_types else None

        # Engine type
        for et, data in self.vehicle_knowledge["engine_types"].items():
            if any(k in q for k in data["keywords"]):
                preferences.engine_type = et
                break

        # Purpose
        purposes = []
        for purpose, data in self.vehicle_knowledge["purposes"].items():
            if any(k in q for k in data["keywords"]):
                purposes.append(purpose)
        preferences.purposes = purposes if purposes else None

        return preferences

    def calculate_match_score(self, listing: VehicleListingOut, preferences: ExtractedPreferences) -> float:
        score = 0
        if preferences.vehicle_type and listing.vehicle.vehicle_type == preferences.vehicle_type:
            score += 30
        if preferences.body_types and listing.vehicle.body_type in preferences.body_types:
            score += 20
        if preferences.engine_type and listing.vehicle.engine_type == preferences.engine_type:
            score += 15
        return min(score, 100)

    def get_recommendations(self, db: Session, query: str, limit: int = 10):
        preferences = self.extract_preferences(query)

        db_query = db.query(VehicleListing).join(Vehicle).join(User)
        listings = db_query.all()

        recs = []
        for l in listings:
            l_out = VehicleListingOut.model_validate(l)
            score = self.calculate_match_score(l_out, preferences)
            if score > 20:
                listing_dict = l_out.model_dump()
                # Add user info so frontend can access it
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
            "query_analysis": f"Processed '{query}'",
            "extracted_preferences": {
                "vehicle_type": preferences.vehicle_type.value if preferences.vehicle_type else None,
                "body_types": [bt.value for bt in preferences.body_types] if preferences.body_types else None,
                "engine_type": preferences.engine_type.value if preferences.engine_type else None,
                "purposes": preferences.purposes,
                "confidence_score": preferences.confidence_score
            }
    }

# Global service instance
nlp_service = NLPRecommendationService()