from pydantic import BaseModel, Field
from typing import Optional

from app.enum import VehicleType, EngineType, BodyType

class VehicleBase(BaseModel):
    vehicle_no: str = Field(..., min_length=6, max_length=20, description="Unique vehicle registration number")
    vehicle_type: VehicleType = Field(..., description="Bike or Car)")
    engine_type: EngineType = Field(..., description="Petrol, Diesel, Electric, or Hybrid")
    engine_battery_capacity: str = Field(..., max_length=10, description="Engine or battery capacity in CC or kWh")
    body_type: BodyType = Field(..., description="Vehicle body type like Sedan, SUV, Hatchback, etc.")
    company: str = Field(..., max_length=50, description="Vehicle brand or manufacturer")
    model_name: str = Field(..., max_length=50, description="Vehicle model name")

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    vehicle_type: Optional[VehicleType] = None
    engine_type: Optional[EngineType] = None
    engine_battery_capacity: Optional[str] = Field(None, max_length=10)
    body_type: Optional[BodyType] = None
    company: Optional[str] = Field(None, max_length=50)
    model_name: Optional[str] = Field(None, max_length=50)

class VehicleOut(VehicleBase):
    id: int
    vehicle_no: str
    vehicle_type: VehicleType
    engine_type: EngineType
    engine_battery_capacity: str
    body_type: BodyType
    company: str
    model_name: str

    model_config = {
        "from_attributes": True
    }