from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

from app.enum import ListingType, MajorCities

class VehicleListing(Base):
    __tablename__ = "vehicle_listings"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to the Vehicle table
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), unique=True, nullable=False)
    vehicle = relationship("Vehicle", back_populates="listings")

    # Foreign key to the User table
    listed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="vehicle_listings")

    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    listing_type = Column(Enum(ListingType), nullable=False)
    price = Column(Float, nullable=False)
    location = Column(Enum(MajorCities), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)