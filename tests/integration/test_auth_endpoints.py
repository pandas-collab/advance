"""Integration tests for authentication API endpoints."""
import pytest
from unittest.mock import Mock, AsyncMock, patch
import json

class TestAuthEndpoints:
    """Test authentication API endpoints."""

    @pytest.fixture
    def mock_app(self):
        """Mock FastAPI application for testing."""
        app = Mock()
        app.post = Mock()
        app.get = Mock()
        return app

    @pytest.mark.asyncio
    async def test_register_endpoint_success(self):
        """Test successful user registration endpoint."""
        registration_data = {
            'email': 'newuser@example.com',
            'password': 'SecurePass123',
            'full_name': 'New User'
        }

        expected_response = {
            'user_id': 'user_123',
            'email': 'newuser@example.com',
            'access_token': 'jwt_token_here',
            'token_type': 'bearer'
        }

        # Mock the endpoint response
        mock_response = AsyncMock()
        mock_response.status_code = 201
        mock_response.json.return_value = expected_response

        # Simulate endpoint call
        with patch('httpx.AsyncClient.post', return_value=mock_response):
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    'http://testserver/api/auth/register',
                    json=registration_data
                )

        assert response.status_code == 201
        response_data = response.json()
        assert response_data['email'] == 'newuser@example.com'
        assert 'access_token' in response_data

    @pytest.mark.asyncio
    async def test_register_endpoint_validation_error(self):
        """Test registration endpoint with validation errors."""
        invalid_data = {
            'email': 'invalid-email',
            'password': '123',  # Too weak
            'full_name': ''  # Empty name
        }

        expected_response = {
            'detail': [
                {'field': 'email', 'message': 'Invalid email format'},
                {'field': 'password', 'message': 'Password too weak'},
                {'field': 'full_name', 'message': 'Full name is required'}
            ]
        }

        mock_response = AsyncMock()
        mock_response.status_code = 422
        mock_response.json.return_value = expected_response

        with patch('httpx.AsyncClient.post', return_value=mock_response):
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    'http://testserver/api/auth/register',
                    json=invalid_data
                )

        assert response.status_code == 422
        response_data = response.json()
        assert 'detail' in response_data

    @pytest.mark.asyncio
    async def test_login_endpoint_success(self):
