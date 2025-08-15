from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from passlib.context import CryptContext
from fastapi import Depends, HTTPException

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash the password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def register_user(fullname: str, phone_number: str, password: str, default_location: str, db: Session = Depends(get_db)) -> dict:
    """Register a new user with hashed password."""
    try:
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if user:
            raise HTTPException(status_code=400, detail="Number already registered")

        hashed_password = get_password_hash(password)
        new_user = User(fullname=fullname,phone_number=phone_number ,password=hashed_password,default_location=default_location)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User registered successfully", "user_id": new_user.id, "fullname": new_user.fullname}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

def login_user(phone_number: str, password: str, db: Session = Depends(get_db)) -> dict:
    """Log in a user by verifying phone number and password."""
    try:
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect password")

        return {"message": "Login successful", "user_id": user.id, "fullname": user.fullname}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")