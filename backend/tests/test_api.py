import requests
import time

def test_api_endpoints():
    base_url = "http://localhost:8000"

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        assert response.status_code == 200
        print(" Health endpoint working")
    except Exception as e:
        print(f" Health endpoint failed: {e}")
        return False

    # Test calculate age endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/calculate-age?birth_date=1990-01-01", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "current_age" in data
        print(" Calculate age endpoint working")
    except Exception as e:
        print(f" Calculate age endpoint failed: {e}")
        return False

    return True

if __name__ == "__main__":
    test_api_endpoints()
