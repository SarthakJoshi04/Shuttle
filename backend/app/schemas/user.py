from pydantic import BaseModel, Field
from typing import Optional

# Enums
from app.enum import MajorCities


class UserBase(BaseModel):
    """Base schema shared by multiple user models."""
    fullname: str = Field(
        ..., min_length=3, max_length=50,
        description="Full name of the user"
    )
    phone_number: str = Field(
        ..., pattern=r'^\+?[1-9]\d{1,14}$',
        description="User phone number in E.164 format"
    )
    default_location: MajorCities = Field(
        ..., description="Default location (city) for the user"
    )


class UserCreate(UserBase):
    """Schema for user registration (includes password)."""
    password: str = Field(
        ..., min_length=8, max_length=255,
        description="Password for the account"
    )


class UserLogin(BaseModel):
    """Schema for user login."""
    phone_number: str = Field(
        ..., description="Phone number in E.164 format"
    )
    password: str = Field(
        ..., description="User account password"
    )


class UserUpdate(BaseModel):
    """Schema for updating user profile details."""
    phone_number: Optional[str] = Field(
        None, pattern=r'^\+?[1-9]\d{1,14}$',
        description="Updated phone number in E.164 format"
    )
    default_location: Optional[MajorCities] = Field(
        None, description="Updated default city for the user"
    )
    password: Optional[str] = Field(
        None, min_length=8, max_length=255,
        description="Updated password"
    )


class UserOut(UserBase):
    """Schema for returning user details (excludes password)."""
    id: int
    fullname: str
    default_location: MajorCities

    model_config = {
        "from_attributes": True  # Allows direct conversion from ORM objects
    }