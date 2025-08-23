from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database import Base

from app.enum import VehicleType, EngineType, BodyType

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_no = Column(String(20), unique=True, nullable=False)
    vehicle_type = Column(Enum(VehicleType), nullable=False)
    engine_type = Column(Enum(EngineType), nullable=False)
    engine_battery_capacity = Column(String(10), nullable=False)
    body_type = Column(Enum(BodyType), nullable=False)
    company = Column(String(50), nullable=False)
    model_name = Column(String(50), nullable=False)

    # One-to-one relationship: vehicle -> listing
    listings = relationship("VehicleListing", back_populates="vehicle", uselist=False)