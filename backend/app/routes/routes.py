from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Request, Query, Form, File, UploadFile
from fastapi.responses import JSONResponse
from app.database import get_db
from app.models.user import User
from app.services.enum_service import (
    get_all_cities, get_all_engine_types, get_all_vehicle_types, get_bike_body_types, get_car_body_types, get_all_listing_types
)
from app.enum import VehicleType, EngineType, BodyType, ListingType
from app.schemas.user import UserCreate, UserOut, UserLogin
from app.services.user_service import register_user, login_user
from app.schemas.vehicle import VehicleCreate
from app.schemas.vehicle_listing import VehicleListingCreate, VehicleListingOut
from app.services.listing_service import create_vehicle_listing, save_uploaded_file
from app.enum import MajorCities
from app.schemas.vehicle_listing import VehicleListingFullCreate
from app.services.user_service import get_current_user_id
from app.schemas.reported_vehicle import ReportedVehicleCreate
from app.services.report_service import report_vehicle as report_vehicle_service

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
    request.session["default_location"] = result["default_location"].value

    user = db.query(User).filter(User.id == result["user_id"]).first()
    return UserOut.model_validate(user)

@router.post("/logout/")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out successfully"}

@router.post("/vehicles/list/", response_model=dict)
async def create_listing(
    user_id: int = Query(..., description="User ID from query parameter"),
    # Vehicle data
    vehicle_no: str = Form(...),
    vehicle_type: str = Form(...),
    engine_type: str = Form(...),
    engine_battery_capacity: str = Form(...),
    body_type: str = Form(...),
    company: str = Form(...),
    model_name: str = Form(...),
    # Listing data
    title: str = Form(...),
    description: str = Form(""),
    listing_type: str = Form(...),
    price: float = Form(...),
    location: str = Form(...),
    # File upload
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Create a new vehicle listing with image upload."""
    
    try:
        # Validate and convert enum values
        vehicle_type_enum = VehicleType(vehicle_type)
        engine_type_enum = EngineType(engine_type)
        body_type_enum = BodyType(body_type)
        listing_type_enum = ListingType(listing_type)
        location_enum = MajorCities(location)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid enum value: {str(e)}")
    
    # Save uploaded image
    image_url = save_uploaded_file(image)
    
    # Create listing data object
    listing_data = VehicleListingFullCreate(
        vehicle_no=vehicle_no,
        vehicle_type=vehicle_type_enum,
        engine_type=engine_type_enum,
        engine_battery_capacity=engine_battery_capacity,
        body_type=body_type_enum,
        company=company,
        model_name=model_name,
        title=title,
        description=description if description else None,
        listing_type=listing_type_enum,
        price=price,
        location=location_enum,
        image_url=image_url
    )
    
    result = create_vehicle_listing(listing_data, user_id, location_enum, db)
    return result

@router.post("/vehicles/report/", response_model=dict)
async def report_vehicle(
    vehicle_no: str = Form(...),
    vehicle_type: str = Form(...),
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    try:
        vehicle_type_enum = VehicleType(vehicle_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid vehicle type")
    
    vehicle_data = ReportedVehicleCreate(
        vehicle_no=vehicle_no,
        vehicle_type=vehicle_type_enum,
        reported_by=user_id
    )
    
    return report_vehicle_service(vehicle_data, user_id, db)