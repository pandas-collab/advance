"""Unit tests for authentication models."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.shared.config.database import Base
from backend.app.auth.models import User, Calculation, APIKey, ValidationRule
import tempfile
import os

class TestUserModel:
    """Test User model functionality."""

    @pytest.fixture
    def db_session(self):
        """Create test database session."""
        # Create temporary SQLite database
        db_fd, db_path = tempfile.mkstemp()
        engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        yield session

        session.close()
        os.close(db_fd)
        os.unlink(db_path)

    def test_create_user(self, db_session):
        """Test user creation."""
        user = User(
            email="test@example.com",
            password_hash="hashed_password",
            full_name="Test User"
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.is_active is True
        assert user.created_at is not None

    def test_user_unique_email(self, db_session):
        """Test that email must be unique."""
        user1 = User(
            email="test@example.com",
            password_hash="hash1",
            full_name="User One"
        )

        user2 = User(
            email="test@example.com",
            password_hash="hash2",
            full_name="User Two"
        )

        db_session.add(user1)
        db_session.commit()

        db_session.add(user2)
        with pytest.raises(Exception):  # Should raise integrity error
            db_session.commit()

class TestCalculationModel:
    """Test Calculation model."""

    @pytest.fixture
    def db_session(self):
        """Create test database session."""
        db_fd, db_path = tempfile.mkstemp()
        engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        yield session

        session.close()
        os.close(db_fd)
        os.unlink(db_path)

    def test_create_calculation(self, db_session):
        """Test calculation creation."""
        calculation = Calculation(
            user_id=1,
            birth_date="1990-01-01",
            target_date="2023-01-01",
            timezone="UTC",
            result_data='{"years": 33, "months": 0, "days": 0}'
        )

        db_session.add(calculation)
        db_session.commit()
        db_session.refresh(calculation)

        assert calculation.id is not None
        assert calculation.user_id == 1
        assert calculation.birth_date == "1990-01-01"
        assert calculation.timezone == "UTC"
        assert calculation.created_at is not None

class TestAPIKeyModel:
    """Test APIKey model."""

    @pytest.fixture
    def db_session(self):
        """Create test database session."""
        db_fd, db_path = tempfile.mkstemp()
        engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        yield session

        session.close()
        os.close(db_fd)
        os.unlink(db_path)

    def test_create_api_key(self, db_session):
        """Test API key creation."""
        api_key = APIKey(
            user_id=1,
            key_name="Test Key",
            key_hash="hashed_key_value",
            permissions='["read", "write"]'
        )

        db_session.add(api_key)
        db_session.commit()
        db_session.refresh(api_key)

        assert api_key.id is not None
        assert api_key.user_id == 1
        assert api_key.key_name == "Test Key"
        assert api_key.is_active is True
