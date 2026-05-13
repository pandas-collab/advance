"""Integration tests for authentication endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.main import app
from backend.app.shared.config.database import Base, get_db
import tempfile
import os

@pytest.fixture
def test_db():
    """Create test database."""
    db_fd, db_path = tempfile.mkstemp()
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(test_db):
    """Create test client with test database."""
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

class TestAuthenticationEndpoints:
    """Test authentication API endpoints."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert "Age Calculator API" in response.text

    def test_user_registration_success(self, client):
        """Test successful user registration."""
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        }

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user_id" in data

    def test_user_registration_duplicate_email(self, client):
        """Test registration with duplicate email."""
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        }

        # Register first user
        response1 = client.post("/api/v1/auth/register", json=user_data)
        assert response1.status_code == 200

        # Try to register with same email
        response2 = client.post("/api/v1/auth/register", json=user_data)
        assert response2.status_code == 400
        assert "already exists" in response2.json()["detail"]

    def test_user_registration_invalid_email(self, client):
        """Test registration with invalid email."""
        user_data = {
            "email": "invalid-email",
            "password": "password123",
            "full_name": "Test User"
        }

        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422  # Validation error

    def test_user_login_success(self, client):
        """Test successful user login."""
        # First register a user
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        }
        client.post("/api/v1/auth/register", json=user_data)

        # Now login
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user_id" in data

    def test_user_login_wrong_password(self, client):
        """Test login with wrong password."""
        # First register a user
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        }
        client.post("/api/v1/auth/register", json=user_data)

        # Try login with wrong password
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }

        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_user_login_nonexistent_user(self, client):
        """Test login with nonexistent user."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "password123"
        }

        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401

    def test_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 403  # No authorization header

    def test_protected_endpoint_with_token(self, client):
        """Test accessing protected endpoint with valid token."""
        # Register and get token
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        }

        register_response = client.post("/api/v1/auth/register", json=user_data)
        token = register_response.json()["access_token"]

        # Use token to access protected endpoint
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/auth/me", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["full_name"] == "Test User"
        assert "user_id" in data
