from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models.user import User
from app.models import user, vehicle, vehicle_listing, reported_vehicle
from app.routes import routes
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define base directory for the application (points to backend/app)
BASE_DIR = Path(__file__).resolve().parent
# Path to favicon file
FAVICON_PATH = BASE_DIR / "static" / "favicon.ico"

# Initialize FastAPI application
app = FastAPI(title="Shuttle Backend")

# Create database tables with error handling
try:
    Base.metadata.create_all(bind=engine) # Create all defined tables in the database
    print("Database tables created successfully")
except Exception as e:
    print(f"Error creating database tables: {str(e)}")
    raise

# Add CORS middleware to allow communication with frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(","), # Allow requests from frontend origin
    allow_credentials=True, # Allow cookies and credentials
    allow_methods=["*"], # Allow all HTTP methods
    allow_headers=["*"], # Allow all headers
)

# Add session middleware for user session management
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv('SESSION_SECRET_KEY'),
    session_cookie=os.getenv('SESSION_COOKIE_NAME', 'session'),
    max_age = int(os.getenv('MAX_SESSION_AGE', 3600))
)

# Include API routes from the routes module
app.include_router(routes.router)

# Route to serve favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(FAVICON_PATH)

# Root endpoint for basic API welcome message
@app.get("/")
async def root():
    return {"message": "Welcome to Shuttle's FastAPI backend!"}

# Endpoint to get current user details from session
@app.get("/me")
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not logged in")
    user = db.query(User).filter(User.id == user_id).first()
    return {"id": user.id, "fullname": user.fullname, "phone_number": user.phone_number}