from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from backend.app.schemas.vehicle import VehicleOut
from backend.app.enum import ListingType, MajorCities

class VehicleListingBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    listing_type: ListingType
    price: float = Field(..., gt=0, description="Listing price must be greater than zero")
    location: MajorCities
    
class VehicleListingCreate(VehicleListingBase):
    vehicle_id: int
    listed_by: int  # This corresponds to the User ID
    
class VehicleListingUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    listing_type: Optional[ListingType] = None
    price: Optional[float] = Field(None, gt=0)

class VehicleListingOut(VehicleListingBase):
    id: int
    vehicle_id: int
    listed_by: int
    created_at: datetime
    vehicle: VehicleOut

    class Config:
        orm_mode = True