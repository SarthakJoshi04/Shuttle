from pydantic import BaseModel, Field
from datetime import datetime

# Enums
from app.enum import VehicleType


class ReportedVehicleBase(BaseModel):
    """Base schema for reported vehicles."""
    vehicle_no: str = Field(
        ..., max_length=20, description="License plate number of the vehicle"
    )
    vehicle_type: VehicleType = Field(
        ..., description="Type of vehicle (Bike or Car)"
    )


class ReportedVehicleCreate(ReportedVehicleBase):
    """Schema for creating a new reported vehicle entry."""
    reported_by: int = Field(
        ..., description="User ID of the person reporting the vehicle"
    )


class ReportedVehicleOut(ReportedVehicleBase):
    """Schema for outputting reported vehicle data."""
    id: int
    reported_by: int
    reported_at: datetime

    model_config = {
        "from_attributes": True  # Allows ORM objects to be parsed directly
    }