# services/listing_service.py
from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.models.vehicle_listing import VehicleListing
from app.schemas.vehicle import VehicleCreate
from app.schemas.vehicle_listing import VehicleListingCreate, VehicleListingOut
from datetime import datetime

from app.models.vehicle import Vehicle
from app.schemas.vehicle_listing import VehicleListingFullCreate
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.enum import MajorCities

def create_vehicle_listing(
    listing_data: VehicleListingFullCreate, 
    user_id: int, 
    location: MajorCities,  # Location parameter
    db: Session  # Remove Depends from service function
) -> dict:
    """Create a vehicle and its listing in a single transaction."""
    try:
        # Check if vehicle already exists
        existing_vehicle = db.query(Vehicle).filter(
            Vehicle.vehicle_no == listing_data.vehicle_no
        ).first()
        
        if existing_vehicle:
            # Check if this vehicle already has a listing
            existing_listing = db.query(VehicleListing).filter(
                VehicleListing.vehicle_id == existing_vehicle.id
            ).first()
            
            if existing_listing:
                raise HTTPException(
                    status_code=400, 
                    detail="This vehicle is already listed"
                )
            
            # Vehicle exists but no listing, create only the listing
            vehicle_id = existing_vehicle.id
        else:
            # Create new vehicle
            vehicle_data = VehicleCreate(
                vehicle_no=listing_data.vehicle_no,
                vehicle_type=listing_data.vehicle_type,
                engine_type=listing_data.engine_type,
                engine_battery_capacity=listing_data.engine_battery_capacity,
                body_type=listing_data.body_type,
                company=listing_data.company,
                model_name=listing_data.model_name
            )
            
            new_vehicle = Vehicle(**vehicle_data.model_dump())
            db.add(new_vehicle)
            db.flush()  # Get the vehicle ID without committing
            vehicle_id = new_vehicle.id
        
        # Create the listing
        new_listing = VehicleListing(
            vehicle_id=vehicle_id,
            listed_by=user_id,
            title=listing_data.title,
            description=listing_data.description,
            listing_type=listing_data.listing_type,
            price=listing_data.price,
            location=location  # Use the location parameter
        )
        
        db.add(new_listing)
        db.commit()
        db.refresh(new_listing)
        
        return {
            "message": "Vehicle listed successfully",
            "vehicle_id": vehicle_id,
            "listing_id": new_listing.id
        }
        
    except IntegrityError as e:
        db.rollback()
        if "vehicle_no" in str(e.orig):
            raise HTTPException(status_code=400, detail="Vehicle number already exists")
        elif "vehicle_id" in str(e.orig):
            raise HTTPException(status_code=400, detail="This vehicle is already listed")
        else:
            raise HTTPException(status_code=400, detail="Database integrity error")
    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create listing: {str(e)}")