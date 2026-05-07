import pytest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create test database BEFORE importing app
SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory:'

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool  # Use StaticPool for in-memory SQLite to avoid connection issues
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Import app components
from app.models import Base
from main import app
from app.database import get_db

# Create tables in test database
Base.metadata.create_all(bind=test_engine)

def override_get_db():
    """Override get_db to use test database session"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Set the dependency override BEFORE creating the TestClient
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Create test client with overridden dependencies"""
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before and after each test"""
    # Drop all tables
    Base.metadata.drop_all(bind=test_engine)
    # Create all tables fresh
    Base.metadata.create_all(bind=test_engine)
    yield
    # Clean up after test
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
