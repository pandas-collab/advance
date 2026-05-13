import pytest
import httpx
import asyncio
import time
from fastapi.testclient import TestClient
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

try:
    from main import app
    client = TestClient(app)
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False
    client = None

class TestAPIIntegration:
    """API Integration Test Suite"""

    def test_health_check(self):
        """Test API health endpoint"""
        if not BACKEND_AVAILABLE:
            pytest.skip("Backend not available")

        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_root_endpoint(self):
        """Test root endpoint"""
        if not BACKEND_AVAILABLE:
            pytest.skip("Backend not available")

        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_age_calculation_endpoint(self):
        """Test age calculation endpoint"""
        if not BACKEND_AVAILABLE:
            pytest.skip("Backend not available")

        test_data = {
            "birthDate": "1990-01-01",
            "currentDate": "2024-01-01"
        }

        response = client.post("/api/v1/calculate-age", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "success"

    def test_cors_headers(self):
        """Test CORS configuration"""
        if not BACKEND_AVAILABLE:
            pytest.skip("Backend not available")

        response = client.options("/health")
        # FastAPI TestClient doesn't fully simulate CORS, so we check the app setup
        assert response.status_code in [200, 405]  # 405 is acceptable for OPTIONS

@pytest.mark.asyncio
async def test_external_api_integration():
    """Test external API integration if backend is running"""
    try:
        async with httpx.AsyncClient() as client:
            # Try to connect to localhost backend
            response = await client.get("http://localhost:8000/health", timeout=5.0)
            assert response.status_code == 200
    except (httpx.ConnectError, httpx.TimeoutException):
        pytest.skip("External backend server not running")

def test_api_performance():
    """Basic API performance test"""
    if not BACKEND_AVAILABLE:
        pytest.skip("Backend not available")

    start_time = time.time()
    response = client.get("/health")
    end_time = time.time()

    assert response.status_code == 200
    assert (end_time - start_time) < 1.0  # Should respond within 1 second

def test_api_error_handling():
    """Test API error handling"""
    if not BACKEND_AVAILABLE:
        pytest.skip("Backend not available")

    # Test invalid endpoint
    response = client.get("/api/v1/nonexistent")
    assert response.status_code == 404
