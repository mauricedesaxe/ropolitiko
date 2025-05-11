# tests/test_server.py
import pytest  # noqa: F401
import unittest.mock

def test_root_endpoint(client):
    """Test the root endpoint returns the expected message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Ropolitiko API"}

def test_health_endpoint(client):
    """Test the health endpoint returns status and resource usage"""
    # Mock psutil to avoid actual system calls in tests
    with unittest.mock.patch("psutil.virtual_memory") as mock_memory, \
         unittest.mock.patch("psutil.cpu_percent") as mock_cpu:
        
        # Configure mocks
        mock_memory.return_value.percent = 50.0
        mock_cpu.return_value = 25.0
        
        # Call the endpoint
        response = client.get("/health")
        
        # Verify response
        assert response.status_code == 200
        assert response.json() == {
            "status": "ok",
            "memory_usage": 50.0,
            "cpu_usage": 25.0
        }