from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.models.user import User
from app.services.location_service import get_all_cities
from app.schemas.user import UserCreate, UserOut, model_validate
from backend.app.services.user_service import register_user, login_user


router = APIRouter()

@router.get("/locations")
def get_locations():
    return get_all_cities()

@router.post("/register/", response_model=UserOut)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    result = register_user(user_data.phone_number, user_data.password, user_data.fullname, user_data.default_location, db)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    user = db.query(User).filter(User.id == result["user_id"]).first()
    return model_validate(UserOut, user)

@router.post("/login/", response_model=UserOut)
async def login(user_data: UserCreate, db: Session = Depends(get_db)):
    result = login_user(user_data.phone_number, user_data.password, db)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    user = db.query(User).filter(User.id == result["user_id"]).first()
    return model_validate(UserOut, user)