from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build the database URL using credentials stored in environment variables
SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@127.0.0.1:3306/{os.getenv('DB_NAME')}"
)

# Create the SQLAlchemy engine instance for connecting to the MySQL database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all the ORM models to inherit from
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()