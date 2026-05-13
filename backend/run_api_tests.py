#!/usr/bin/env python3
"""
Simple API test runner that doesn't require pytest installation
"""
import sys
import os
import time
import threading
import subprocess
import requests

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_fastapi_import():
    """Test if FastAPI can be imported and app can be created"""
    try:
        from main import app
        print(" FastAPI app import successful")
        return True, app
    except ImportError as e:
        print(f" FastAPI import failed: {e}")
        return False, None
    except Exception as e:
        print(f" App creation failed: {e}")
        return False, None

def test_basic_endpoints(app):
    """Test basic endpoints using TestClient"""
    try:
        from fastapi.testclient import TestClient
        client = TestClient(app)

        # Test root endpoint
        response = client.get("/")
        assert response.status_code == 200, f"Root endpoint failed: {response.status_code}"
        print(" Root endpoint test passed")

        # Test health endpoint
        response = client.get("/health")
        assert response.status_code == 200, f"Health endpoint failed: {response.status_code}"
        data = response.json()
        assert data["status"] == "healthy", f"Health check failed: {data}"
        print(" Health endpoint test passed")

        # Test age calculation endpoint
        test_data = {"birthDate": "1990-01-01", "currentDate": "2024-01-01"}
        response = client.post("/api/v1/calculate-age", json=test_data)
        assert response.status_code == 200, f"Age calculation failed: {response.status_code}"
        print(" Age calculation endpoint test passed")

        return True
    except Exception as e:
        print(f" Endpoint testing failed: {e}")
        return False

def main():
    """Run API integration tests"""
    print("=== API INTEGRATION TESTS ===")

    # Test 1: Import and app creation
    success, app = test_fastapi_import()
    if not success:
        print("API_INTEGRATION_TEST: FAILED - Cannot import FastAPI app")
        return 1

    # Test 2: Basic endpoint testing
    if not test_basic_endpoints(app):
        print("API_INTEGRATION_TEST: FAILED - Endpoint tests failed")
        return 1

    print("API_INTEGRATION_TEST: PASSED - All tests successful")
    return 0

if __name__ == "__main__":
    exit(main())
