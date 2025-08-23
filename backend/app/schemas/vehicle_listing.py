from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.schemas.vehicle import VehicleOut
from app.enum import ListingType, MajorCities, VehicleType, EngineType, BodyType

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

class VehicleListingFullCreate(BaseModel):
    # Vehicle details from VehicleCreate
    vehicle_no: str = Field(..., min_length=6, max_length=20, description="Unique vehicle registration number")
    vehicle_type: VehicleType = Field(..., description="Bike or Car")
    engine_type: EngineType = Field(..., description="Petrol, Diesel, Electric, or Hybrid")
    engine_battery_capacity: str = Field(..., max_length=10, description="Engine or battery capacity in CC or kWh")
    body_type: BodyType = Field(..., description="Vehicle body type like Sedan, SUV, Hatchback, etc.")
    company: str = Field(..., max_length=50, description="Vehicle brand or manufacturer")
    model_name: str = Field(..., max_length=50, description="Vehicle model name")

    # Listing details from VehicleListingCreate
    title: str = Field(..., min_length=5, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    listing_type: ListingType
    price: float = Field(..., gt=0, description="Listing price must be greater than zero")
    location: MajorCities  # Add location field to the schema

class VehicleListingOut(VehicleListingBase):
    id: int
    vehicle_id: int
    listed_by: int
    created_at: datetime
    vehicle: VehicleOut

    model_config = {
        "from_attributes": True
    }