from pathlib import Path
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app.models.user import User
from app.models import user, vehicle, vehicle_listing, reported_vehicle
from app.routes import routes


# Load environment variables from .env file
load_dotenv()

# Define base directory for the application
BASE_DIR = Path(__file__).resolve().parent
FAVICON_PATH = BASE_DIR / "static" / "favicon.ico"

# Initialize FastAPI application
app = FastAPI(title="Shuttle Backend")


# ---------------------- Database ----------------------
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Error creating database tables: {str(e)}")
    raise


# ---------------------- Middleware ----------------------
# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session middleware for user sessions
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY"),
    session_cookie=os.getenv("SESSION_COOKIE_NAME", "session"),
    max_age=int(os.getenv("MAX_SESSION_AGE", 3600)),
)


# ---------------------- Routes ----------------------
# Include API routes from routes module
app.include_router(routes.router)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# ---------------------- Endpoints ----------------------
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Serve the favicon.ico file."""
    return FileResponse(FAVICON_PATH)


@app.get("/")
async def root():
    """Root endpoint for API welcome message."""
    return {"message": "Welcome to Shuttle's FastAPI backend!"}


@app.get("/me")
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    """Get currently logged-in user information from session."""
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not logged in")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "fullname": user.fullname,
        "phone_number": user.phone_number,
    }