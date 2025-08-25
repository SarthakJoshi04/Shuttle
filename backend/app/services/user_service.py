from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext

# Project-specific imports
from app.models.user import User

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Hash the password using bcrypt.

    Args:
        password (str): Plain text password.

    Returns:
        str: Hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): User-provided password.
        hashed_password (str): Stored hashed password.

    Returns:
        bool: True if password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def register_user(
    fullname: str,
    phone_number: str,
    password: str,
    default_location: str,
    db: Session
) -> dict:
    """
    Register a new user with hashed password.

    Args:
        fullname (str): Full name of the user.
        phone_number (str): Phone number of the user.
        password (str): Plain text password.
        default_location (str): Default city/location of the user.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: Confirmation message and user details.

    Raises:
        HTTPException: If user already exists or database error occurs.
    """
    try:
        # Check if phone number is already registered
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if user:
            raise HTTPException(status_code=400, detail="Number already registered")

        # Hash password and create user
        hashed_password = get_password_hash(password)
        new_user = User(
            fullname=fullname,
            phone_number=phone_number,
            password=hashed_password,
            default_location=default_location
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "user_id": new_user.id,
            "fullname": new_user.fullname
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


def login_user(
    phone_number: str,
    password: str,
    db: Session
) -> dict:
    """
    Log in a user by verifying phone number and password.

    Args:
        phone_number (str): User's phone number.
        password (str): Plain text password.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: Login confirmation and user details.

    Raises:
        HTTPException: If user not found, incorrect password, or database error occurs.
    """
    try:
        # Fetch user by phone number
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect password")

        return {
            "message": "Login successful",
            "user_id": user.id,
            "fullname": user.fullname,
            "default_location": user.default_location
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")