from typing import Optional
from pydantic import BaseModel, Field

# Enums
from app.enum import VehicleType, EngineType, BodyType


class VehicleBase(BaseModel):
    """Base schema shared by multiple vehicle models."""
    
    vehicle_no: str = Field(
        ..., min_length=6, max_length=20,
        description="Unique vehicle registration number"
    )
    vehicle_type: VehicleType = Field(
        ..., description="Type of vehicle (Bike or Car)"
    )
    engine_type: EngineType = Field(
        ..., description="Engine type (Petrol, Diesel, Electric, or Hybrid)"
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


class VehicleCreate(VehicleBase):
    """Schema for creating a new vehicle entry."""
    pass


class VehicleUpdate(BaseModel):
    """Schema for updating an existing vehicle (all fields optional)."""
    
    vehicle_type: Optional[VehicleType] = Field(
        None, description="Updated type of vehicle (Bike or Car)"
    )
    engine_type: Optional[EngineType] = Field(
        None, description="Updated engine type"
    )
    engine_battery_capacity: Optional[str] = Field(
        None, max_length=10, description="Updated engine or battery capacity"
    )
    body_type: Optional[BodyType] = Field(
        None, description="Updated vehicle body type"
    )
    company: Optional[str] = Field(
        None, max_length=50, description="Updated vehicle brand or manufacturer"
    )
    model_name: Optional[str] = Field(
        None, max_length=50, description="Updated vehicle model name"
    )


class VehicleOut(VehicleBase):
    """Schema for returning vehicle details (API response)."""
    
    id: int = Field(..., description="ID of the vehicle")
    vehicle_no: str
    vehicle_type: VehicleType
    engine_type: EngineType
    engine_battery_capacity: str
    body_type: BodyType
    company: str
    model_name: str

    model_config = {
        "from_attributes": True  # Enables ORM mode (from SQLAlchemy objects)
    }