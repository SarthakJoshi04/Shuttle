from pathlib import Path
import uuid

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Project-specific models and schemas
from app.models.vehicle import Vehicle
from app.models.vehicle_listing import VehicleListing
from app.models.reported_vehicle import ReportedVehicle
from app.schemas.vehicle import VehicleCreate
from app.schemas.vehicle_listing import VehicleListingFullCreate
from app.enum import MajorCities

# --------------------------
# File upload configuration
# --------------------------

UPLOAD_DIR = Path("uploads/vehicles")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def save_uploaded_file(file: UploadFile) -> str:
    """
    Save an uploaded image file and return its URL.

    Args:
        file (UploadFile): Uploaded file from the request.

    Returns:
        str: URL path to the saved file.

    Raises:
        HTTPException: If file type is invalid or saving fails.
    """
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    return f"/uploads/vehicles/{unique_filename}"


def create_vehicle_listing(
    listing_data: VehicleListingFullCreate,
    user_id: int,
    location: MajorCities,
    db: Session
) -> dict:
    """
    Create a vehicle and its listing in a single transaction.

    Args:
        listing_data (VehicleListingFullCreate): Data for the vehicle and listing.
        user_id (int): ID of the user creating the listing.
        location (MajorCities): City where the vehicle is located.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: Success message and created IDs.

    Raises:
        HTTPException: On validation, integrity, or server errors.
    """
    try:
        # Check if vehicle has been reported stolen
        reported_vehicle = db.query(ReportedVehicle).filter(
            ReportedVehicle.vehicle_no == listing_data.vehicle_no,
            ReportedVehicle.vehicle_type == listing_data.vehicle_type.value
        ).first()

        if reported_vehicle:
            raise HTTPException(
                status_code=403,
                detail=(
                    "This vehicle has been reported as stolen and cannot be listed. "
                    "If this is your vehicle, please contact authorities."
                )
            )

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

            # Vehicle exists but no listing
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
            db.flush()  # Obtain vehicle ID without committing
            vehicle_id = new_vehicle.id

        # Create the listing
        new_listing = VehicleListing(
            vehicle_id=vehicle_id,
            listed_by=user_id,
            title=listing_data.title,
            description=listing_data.description,
            listing_type=listing_data.listing_type,
            price=listing_data.price,
            location=location,
            image_url=listing_data.image_url
        )

        db.add(new_listing)
        db.commit()
        db.refresh(new_listing)

        return {
            "message": "Vehicle listed successfully",
            "vehicle_id": vehicle_id,
            "listing_id": new_listing.id,
            "image_url": listing_data.image_url
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