from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.database import engine, Base
from backend.app.models import user, vehicle, vehicle_listing, reported_vehicle
from backend.app.routes import routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables if they do not exist on startup
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables are ready!")
    yield

app = FastAPI(title="Shuttle Backend", lifespan=lifespan)

# Enable CORS to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

# Serve Favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI backend!"}