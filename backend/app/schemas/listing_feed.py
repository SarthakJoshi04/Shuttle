from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Enums
from app.enum import ListingType, MajorCities

# Nested schema
from app.schemas.vehicle import VehicleOut


class UserPublicOut(BaseModel):
    """Public user information shown in feeds and listings."""
    id: int
    fullname: str
    phone_number: Optional[str] = None  # Only returned if user is logged in

    model_config = {
        "from_attributes": True  # Allows model creation directly from ORM objects
    }


class VehicleListingFeedOut(BaseModel):
    """Schema for vehicle listing feed output, including relations."""
    # From VehicleListing table
    id: int
    title: str
    description: Optional[str]
    listing_type: ListingType
    price: float
    location: MajorCities
    image_url: Optional[str]
    created_at: datetime

    # Related objects
    vehicle: VehicleOut
    user: UserPublicOut

    model_config = {
        "from_attributes": True  # Enables validation from ORM objects
    }