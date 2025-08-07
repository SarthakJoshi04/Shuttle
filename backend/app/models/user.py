from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from backend.app.database import Base

from backend.app.enum import MajorCities

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100), nullable=False)
    phone_number = Column(String(15), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    default_location = Column(Enum(MajorCities), nullable=False)

    # One-to-many relationship: user -> reported vehicles
    reported_vehicles = relationship("ReportedVehicle", back_populates="reporter")

    # One-to-many relationship: user -> vehicle listings
    vehicle_listings = relationship("VehicleListing", back_populates="user")