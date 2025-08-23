from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

from app.enum import VehicleType

class ReportedVehicle(Base):
    __tablename__ = "reported_vehicles"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_no = Column(String(20), nullable=False)
    vehicle_type = Column(Enum(VehicleType), nullable=False)

    # Foreign key to the User who reported this vehicle
    reported_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    reporter = relationship("User", back_populates="reported_vehicles")