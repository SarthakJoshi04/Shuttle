from pydantic import BaseModel, Field
from typing import Optional

from backend.app.enum import MajorCities

class UserBase(BaseModel):
    fullname: str = Field(..., min_length=3, max_length=50)
    phone_number: str = Field(..., regex=r'^\+?[1-9]\d{1,14}$')  # E.164 format
    default_location: MajorCities = Field(..., description="Default location for the user")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255)

class UserUpdate(BaseModel):
    phone_number: Optional[str] = Field(None, regex=r'^\+?[1-9]\d{1,14}$')  # E.164 format
    default_location: Optional[MajorCities] = Field(None, description="Default location for the user")
    password: Optional[str] = Field(None, min_length=8, max_length=255)
    
class UserOut(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }