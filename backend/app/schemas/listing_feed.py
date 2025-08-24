from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.enum import ListingType, MajorCities
from app.schemas.vehicle import VehicleOut

class UserPublicOut(BaseModel):
    id: int
    fullname: str
    phone_number: Optional[str] = None 

    model_config = {
        "from_attributes": True
    }

class VehicleListingFeedOut(BaseModel):
    # from VehicleListing
    id: int
    title: str
    description: Optional[str]
    listing_type: ListingType
    price: float
    location: MajorCities
    image_url: Optional[str]
    created_at: datetime

    # relations
    vehicle: VehicleOut
    user: UserPublicOut

    model_config = {
        "from_attributes": True
    }