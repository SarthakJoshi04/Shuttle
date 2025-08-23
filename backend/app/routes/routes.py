from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from app.database import get_db
from app.models.user import User
from app.services.enum_service import (
    get_all_cities, get_all_engine_types, get_all_vehicle_types, get_bike_body_types, get_car_body_types, get_all_listing_types
)
from app.schemas.user import UserCreate, UserOut, UserLogin
from app.services.user_service import register_user, login_user
from app.schemas.vehicle import VehicleCreate
from app.schemas.vehicle_listing import VehicleListingCreate, VehicleListingOut
from app.services.listing_service import create_vehicle_listing
from app.enum import MajorCities
from app.schemas.vehicle_listing import VehicleListingFullCreate
from app.services.user_service import get_current_user_id

router = APIRouter()

@router.get("/locations")
def locations():
    return get_all_cities()

@router.get("/vehicle-types")
def vehicle_types():
    return get_all_vehicle_types()

@router.get("/engine-types")
def engine_types():
    return get_all_engine_types()

@router.get("/car-body-types")
def car_body_types():
    return get_car_body_types()

@router.get("/bike-body-types")
def bike_body_types():
    return get_bike_body_types()

@router.get("/listing-types")
def listing_types():
    return get_all_listing_types()

@router.post("/register/", response_model=UserOut)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    result = register_user(
        fullname=user_data.fullname,
        phone_number=user_data.phone_number,
        password=user_data.password,
        default_location=user_data.default_location,
        db=db
    )
    
    user = db.query(User).filter(User.id == result["user_id"]).first()
    return UserOut.model_validate(user)

@router.post("/login/", response_model=UserOut)
async def login(user_data: UserLogin, request: Request, db: Session = Depends(get_db)):
    result = login_user(user_data.phone_number, user_data.password, db)

    request.session["user_id"] = result["user_id"]
    request.session["fullname"] = result["fullname"]
    request.session["default_location"] = result["default_location"].name

    user = db.query(User).filter(User.id == result["user_id"]).first()
    return UserOut.model_validate(user)

@router.post("/logout/")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out successfully"}

# Fixed route to match frontend call
@router.post("/vehicles/list/", response_model=dict)
async def create_listing(
    listing_data: VehicleListingFullCreate,
    user_id: int = Query(..., description="User ID from query parameter"),
    db: Session = Depends(get_db)
):
    """Create a new vehicle listing."""
    
    # Validate location from the listing_data
    try:
        location_enum = MajorCities(listing_data.location)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location")
    
    result = create_vehicle_listing(listing_data, user_id, location_enum, db)
    return result