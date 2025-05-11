import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Now we can import app modules
from app.api.server import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)