"""Unit tests for authentication models."""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from backend.app.auth.models import User, ApiKey, ValidationRule
from backend.app.auth.service import AuthService

class TestUserModel:
    """Test cases for User model."""

    def test_user_creation(self):
        """Test user model creation."""
        user_data = {
            'email': 'test@example.com',
            'full_name': 'Test User',
            'password_hash': 'hashed_password',
            'is_admin': False
        }

        user = User(**user_data)

        assert user.email == 'test@example.com'
        assert user.full_name == 'Test User'
        assert user.is_admin is False

    def test_user_email_validation(self):
        """Test user email validation."""
        with pytest.raises(ValueError):
            User(
                email='invalid_email',
                full_name='Test User',
                password_hash='hashed_password'
            )

    def test_user_password_hashing(self):
        """Test password hashing functionality."""
        user = User(
            email='test@example.com',
            full_name='Test User',
            password_hash='plain_password'
        )

        # Assuming password gets hashed on creation
        assert user.password_hash != 'plain_password'

    def test_user_admin_default(self):
        """Test user admin flag default value."""
        user = User(
            email='test@example.com',
            full_name='Test User',
            password_hash='hashed_password'
        )

        assert user.is_admin is False

    def test_user_timestamps(self):
        """Test user timestamp fields."""
        user = User(
            email='test@example.com',
            full_name='Test User',
            password_hash='hashed_password'
        )

        assert hasattr(user, 'created_at')
        assert hasattr(user, 'updated_at')

class TestApiKeyModel:
    """Test cases for ApiKey model."""

    def test_api_key_creation(self):
        """Test API key model creation."""
        api_key_data = {
            'name': 'Test API Key',
            'key_hash': 'hashed_key',
            'permissions': ['read', 'write'],
            'rate_limit': 1000,
            'is_active': True
        }

        api_key = ApiKey(**api_key_data)

        assert api_key.name == 'Test API Key'
        assert api_key.rate_limit == 1000
        assert api_key.is_active is True

    def test_api_key_permissions(self):
        """Test API key permissions handling."""
        api_key = ApiKey(
            name='Test Key',
            key_hash='hash',
            permissions=['calculations:read', 'calculations:write'],
            rate_limit=100
        )

        assert 'calculations:read' in api_key.permissions
        assert 'calculations:write' in api_key.permissions

    def test_api_key_expiration(self):
        """Test API key expiration."""
        future_date = datetime.utcnow() + timedelta(days=30)
        api_key = ApiKey(
            name='Test Key',
            key_hash='hash',
            permissions=['read'],
            rate_limit=100,
            expires_at=future_date
        )

        assert api_key.expires_at == future_date
        assert not api_key.is_expired()

    def test_api_key_rate_limiting(self):
        """Test API key rate limiting."""
        api_key = ApiKey(
            name='Test Key',
            key_hash='hash',
            permissions=['read'],
            rate_limit=10
        )

        assert api_key.rate_limit == 10
        assert api_key.can_make_request()

class TestValidationRuleModel:
    """Test cases for ValidationRule model."""

    def test_validation_rule_creation(self):
        """Test validation rule model creation."""
        rule_data = {
            'name': 'Age Limit Rule',
            'description': 'Limits maximum age calculation',
            'rule_config': {'max_years': 150},
            'is_active': True
        }

        rule = ValidationRule(**rule_data)

        assert rule.name == 'Age Limit Rule'
        assert rule.rule_config['max_years'] == 150
        assert rule.is_active is True

    def test_validation_rule_config(self):
        """Test validation rule configuration."""
        rule = ValidationRule(
            name='Date Range Rule',
            description='Validates date ranges',
            rule_config={
                'min_date': '1900-01-01',
                'max_date': '2100-12-31',
                'allow_future': False
            },
            is_active=True
        )

        config = rule.rule_config
        assert config['min_date'] == '1900-01-01'
        assert config['allow_future'] is False

    def test_validation_rule_priority(self):
        """Test validation rule priority ordering."""
        rule1 = ValidationRule(
            name='Rule 1',
            description='First rule',
            rule_config={},
            priority=1,
            is_active=True
        )

        rule2 = ValidationRule(
            name='Rule 2',
            description='Second rule',
            rule_config={},
            priority=2,
            is_active=True
        )

        assert rule1.priority < rule2.priority

    def test_validation_rule_deactivation(self):
        """Test validation rule deactivation."""
        rule = ValidationRule(
            name='Test Rule',
            description='Test rule',
            rule_config={},
            is_active=True
        )

        rule.is_active = False
        assert rule.is_active is False

class TestAuthService:
    """Test cases for AuthService."""

    def setup_method(self):
        """Setup test fixtures."""
        self.auth_service = AuthService()

    @pytest.mark.asyncio
    async def test_create_user(self):
        """Test user creation through auth service."""
        user_data = {
            'email': 'newuser@example.com',
            'password': 'secure_password',
            'full_name': 'New User'
        }

        with patch.object(self.auth_service, 'hash_password') as mock_hash:
            mock_hash.return_value = 'hashed_password'

            with patch.object(self.auth_service, 'save_user') as mock_save:
                mock_save.return_value = Mock(user_id='user-123')

                user = await self.auth_service.create_user(user_data)

                assert user.user_id == 'user-123'
                mock_hash.assert_called_once_with('secure_password')

    @pytest.mark.asyncio
    async def test_authenticate_user_valid(self):
        """Test valid user authentication."""
        with patch.object(self.auth_service, 'get_user_by_email') as mock_get:
            mock_user = Mock()
            mock_user.password_hash = 'correct_hash'
            mock_get.return_value = mock_user

            with patch.object(self.auth_service, 'verify_password') as mock_verify:
                mock_verify.return_value = True

                user = await self.auth_service.authenticate_user('test@example.com', 'password')

                assert user == mock_user

    @pytest.mark.asyncio
    async def test_authenticate_user_invalid(self):
        """Test invalid user authentication."""
        with patch.object(self.auth_service, 'get_user_by_email') as mock_get:
            mock_get.return_value = None

            user = await self.auth_service.authenticate_user('test@example.com', 'password')

            assert user is None

    def test_generate_jwt_token(self):
        """Test JWT token generation."""
        user_data = {'user_id': 'user-123', 'email': 'test@example.com'}

        token = self.auth_service.generate_jwt_token(user_data)

        assert token is not None
        assert isinstance(token, str)

    def test_verify_jwt_token(self):
        """Test JWT token verification."""
        user_data = {'user_id': 'user-123', 'email': 'test@example.com'}
        token = self.auth_service.generate_jwt_token(user_data)

        decoded = self.auth_service.verify_jwt_token(token)

        assert decoded['user_id'] == 'user-123'
        assert decoded['email'] == 'test@example.com'
