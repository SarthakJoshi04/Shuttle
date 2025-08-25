from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

# Project-specific Enums and nested schemas
from app.schemas.vehicle import VehicleOut
from app.enum import ListingType, MajorCities, VehicleType, EngineType, BodyType


class VehicleListingBase(BaseModel):
    """Base schema shared by multiple vehicle listing models."""
    
    title: str = Field(
        ..., min_length=5, max_length=100,
        description="Title of the vehicle listing"
    )
    description: Optional[str] = Field(
        None, max_length=1000,
        description="Optional description of the vehicle listing"
    )
    listing_type: ListingType = Field(
        ..., description="Type of listing (RENTAL or SALE)"
    )
    price: float = Field(
        ..., gt=0,
        description="Listing price must be greater than zero"
    )
    location: MajorCities = Field(
        ..., description="City where the vehicle is located"
    )


class VehicleListingCreate(VehicleListingBase):
    """Schema for creating a new vehicle listing (requires existing vehicle_id)."""
    
    vehicle_id: int = Field(
        ..., description="ID of the vehicle being listed"
    )
    image_url: Optional[str] = Field(
        None, max_length=255,
        description="URL of the vehicle image"
    )
    listed_by: int = Field(
        ..., description="User ID of the person creating the listing"
    )


class VehicleListingUpdate(BaseModel):
    """Schema for updating an existing vehicle listing (all fields optional)."""
    
    title: Optional[str] = Field(
        None, min_length=5, max_length=100,
        description="Updated title of the listing"
    )
    description: Optional[str] = Field(
        None, max_length=1000,
        description="Updated description of the listing"
    )
    listing_type: Optional[ListingType] = Field(
        None, description="Updated type of listing (RENTAL or SALE)"
    )
    price: Optional[float] = Field(
        None, gt=0,
        description="Updated price of the listing"
    )
    image_url: Optional[str] = Field(
        None, max_length=255,
        description="Updated URL of the vehicle image"
    )


class VehicleListingFullCreate(BaseModel):
    """Schema for creating a vehicle and listing together in one request."""
    
    # Vehicle details
    vehicle_no: str = Field(
        ..., min_length=6, max_length=20,
        description="Unique vehicle registration number"
    )
    vehicle_type: VehicleType = Field(
        ..., description="Bike or Car"
    )
    engine_type: EngineType = Field(
        ..., description="Petrol, Diesel, Electric, or Hybrid"
    )
    engine_battery_capacity: str = Field(
        ..., max_length=10,
        description="Engine or battery capacity in CC or kWh"
    )
    body_type: BodyType = Field(
        ..., description="Vehicle body type like Sedan, SUV, Hatchback, etc."
    )
    company: str = Field(
        ..., max_length=50,
        description="Vehicle brand or manufacturer"
    )
    model_name: str = Field(
        ..., max_length=50,
        description="Vehicle model name"
    )

    # Listing details
    title: str = Field(
        ..., min_length=5, max_length=100,
        description="Title of the vehicle listing"
    )
    image_url: Optional[str] = Field(
        None, max_length=255,
        description="URL of the vehicle image"
    )
    description: Optional[str] = Field(
        None, max_length=1000,
        description="Optional description of the listing"
    )
    listing_type: ListingType = Field(
        ..., description="Type of listing (RENTAL or SALE)"
    )
    price: float = Field(
        ..., gt=0,
        description="Listing price must be greater than zero"
    )
    location: MajorCities = Field(
        ..., description="City where the vehicle is located"
    )


class VehicleListingOut(VehicleListingBase):
    """Schema for API response, including nested vehicle details."""
    
    id: int = Field(..., description="ID of the listing")
    vehicle_id: int = Field(..., description="ID of the vehicle being listed")
    listed_by: int = Field(..., description="ID of the user who created the listing")
    created_at: datetime = Field(..., description="Timestamp when the listing was created")
    image_url: Optional[str] = Field(
        None, description="URL of the vehicle image"
    )
    vehicle: VehicleOut = Field(..., description="Nested vehicle details")

    model_config = {
        "from_attributes": True  # Enables ORM parsing directly from SQLAlchemy objects
    }