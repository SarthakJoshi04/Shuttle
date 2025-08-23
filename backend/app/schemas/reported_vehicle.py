from pydantic import BaseModel, Field

from app.enum import VehicleType

class ReportedVehicleBase(BaseModel):
    vehicle_no: str = Field(..., max_length=20, description="License plate number of the vehicle")
    vehicle_type: VehicleType = Field(..., description="Bike or Car")

class ReportedVehicleCreate(ReportedVehicleBase):
    reported_by: int = Field(..., description="User ID of the person reporting the vehicle")

class ReportedVehicleOut(ReportedVehicleBase):
    id: int
    reported_by: int

    model_config = {
        "from_attributes": True
    }