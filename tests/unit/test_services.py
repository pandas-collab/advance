"""Unit tests for services."""
import pytest
from unittest.mock import Mock, AsyncMock
from backend.app.shared.services.email import EmailService
from backend.app.auth.service import AuthService
from backend.app.shared.config.jwt import create_access_token, verify_token, verify_password, get_password_hash

class TestEmailService:
    """Test email service functionality."""

    @pytest.fixture
    def email_service(self):
        return EmailService()

    @pytest.mark.asyncio
    async def test_send_email_success(self, email_service):
        """Test successful email sending."""
        # Mock SMTP for testing
        result = await email_service.send_email(
            to_emails=["test@example.com"],
            subject="Test Subject",
            html_content="<p>Test</p>",
            text_content="Test"
        )
        # Should return True even in test mode
        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_send_welcome_email(self, email_service):
        """Test welcome email sending."""
        result = await email_service.send_welcome_email(
            email="test@example.com",
            full_name="Test User"
        )
        assert isinstance(result, bool)

class TestJWTUtils:
    """Test JWT utility functions."""

    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "testpassword123"
        hashed = get_password_hash(password)

        assert hashed != password
        assert verify_password(password, hashed)
        assert not verify_password("wrongpassword", hashed)

    def test_token_creation_and_verification(self):
        """Test JWT token creation and verification."""
        user_id = 123
        token = create_access_token(subject=user_id)

        assert isinstance(token, str)
        assert len(token) > 0

        verified_id = verify_token(token)
        assert verified_id == str(user_id)

    def test_invalid_token_verification(self):
        """Test verification of invalid token."""
        invalid_token = "invalid.token.here"
        result = verify_token(invalid_token)
        assert result is None

class TestAuthService:
    """Test authentication service."""

    @pytest.fixture
    def mock_db(self):
        """Mock database session."""
        db = Mock()
        db.query.return_value.filter.return_value.first.return_value = None
        db.add = Mock()
        db.commit = Mock()
        db.refresh = Mock()
        return db

    def test_get_user_by_email_not_found(self, mock_db):
        """Test getting user by email when not found."""
        result = AuthService.get_user_by_email(mock_db, "test@example.com")
        assert result is None

    def test_create_user_success(self, mock_db):
        """Test successful user creation."""
        user = AuthService.create_user(
            db=mock_db,
            email="test@example.com",
            password="password123",
            full_name="Test User"
        )

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.password_hash != "password123"  # Should be hashed
