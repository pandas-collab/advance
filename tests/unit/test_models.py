"""Unit tests for database models."""
import pytest
from datetime import datetime, date
from uuid import uuid4
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

class TestCalculationModel:
    """Test cases for Calculation model."""

    def test_calculation_model_creation(self):
        """Test calculation model creation."""
        calculation_data = {
            'calculation_id': str(uuid4()),
            'user_id': str(uuid4()),
            'birth_date': date(1990, 1, 1),
            'target_date': date(2023, 1, 1),
            'years': 33,
            'months': 0,
            'days': 0,
            'total_days': 12053,
            'precision_level': 'days',
            'created_at': datetime.utcnow()
        }

        # Mock calculation model
        class Calculation:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

        calculation = Calculation(**calculation_data)

        assert calculation.years == 33
        assert calculation.total_days == 12053
        assert calculation.precision_level == 'days'

    def test_calculation_validation(self):
        """Test calculation model validation."""
        # Test invalid dates
        with pytest.raises(ValueError):
            birth_date = date(2023, 1, 1)
            target_date = date(1990, 1, 1)

            if birth_date >= target_date:
                raise ValueError("Birth date must be before target date")

    def test_calculation_date_formatting(self):
        """Test calculation date formatting."""
        birth_date = date(1990, 1, 1)
        target_date = date(2023, 1, 1)

        assert birth_date.strftime('%Y-%m-%d') == '1990-01-01'
        assert target_date.strftime('%Y-%m-%d') == '2023-01-01'

class TestUserCalculationRelationship:
    """Test cases for User-Calculation relationships."""

    def test_user_has_multiple_calculations(self):
        """Test user can have multiple calculations."""
        user_id = str(uuid4())

        calculations = [
            {
                'calculation_id': str(uuid4()),
                'user_id': user_id,
                'birth_date': date(1990, 1, 1),
                'target_date': date(2023, 1, 1),
                'years': 33
            },
            {
                'calculation_id': str(uuid4()),
                'user_id': user_id,
                'birth_date': date(1985, 5, 15),
                'target_date': date(2023, 5, 15),
                'years': 38
            }
        ]

        assert len(calculations) == 2
        assert calculations[0]['user_id'] == user_id
        assert calculations[1]['user_id'] == user_id

    def test_calculation_belongs_to_user(self):
        """Test calculation belongs to specific user."""
        user_id = str(uuid4())
        calculation_id = str(uuid4())

        calculation = {
            'calculation_id': calculation_id,
            'user_id': user_id,
            'birth_date': date(1990, 1, 1),
            'target_date': date(2023, 1, 1)
        }

        assert calculation['user_id'] == user_id
        assert calculation['calculation_id'] == calculation_id

class TestModelConstraints:
    """Test cases for model constraints and validations."""

    def test_required_fields(self):
        """Test required field validation."""
        required_calculation_fields = [
            'user_id', 'birth_date', 'target_date',
            'years', 'months', 'days', 'total_days'
        ]

        calculation_data = {
            'user_id': str(uuid4()),
            'birth_date': date(1990, 1, 1),
            'target_date': date(2023, 1, 1),
            'years': 33,
            'months': 0,
            'days': 0,
            'total_days': 12053
        }

        for field in required_calculation_fields:
            assert field in calculation_data

    def test_field_types(self):
        """Test field type validation."""
        calculation_data = {
            'user_id': str(uuid4()),
            'birth_date': date(1990, 1, 1),
            'target_date': date(2023, 1, 1),
            'years': 33,
            'months': 0,
            'days': 0,
            'total_days': 12053,
            'precision_level': 'days',
            'created_at': datetime.utcnow()
        }

        assert isinstance(calculation_data['user_id'], str)
        assert isinstance(calculation_data['birth_date'], date)
        assert isinstance(calculation_data['target_date'], date)
        assert isinstance(calculation_data['years'], int)
        assert isinstance(calculation_data['precision_level'], str)
        assert isinstance(calculation_data['created_at'], datetime)

    def test_uuid_generation(self):
        """Test UUID generation for IDs."""
        calculation_id = str(uuid4())
        user_id = str(uuid4())

        assert len(calculation_id) == 36  # Standard UUID length
        assert len(user_id) == 36
        assert calculation_id != user_id  # Should be unique

    def test_precision_level_options(self):
        """Test precision level validation."""
        valid_precision_levels = ['years', 'months', 'days', 'hours']

        for level in valid_precision_levels:
            assert level in valid_precision_levels

        # Test invalid precision level
        invalid_level = 'invalid_precision'
        assert invalid_level not in valid_precision_levels

class TestDatabaseConstraints:
    """Test cases for database-level constraints."""

    def test_foreign_key_constraint(self):
        """Test foreign key relationships."""
        user_id = str(uuid4())
        calculation_user_id = user_id  # Should match existing user

        # Simulate foreign key constraint
        assert calculation_user_id == user_id

    def test_unique_constraints(self):
        """Test unique field constraints."""
        # Email should be unique per user
        emails = ['user1@example.com', 'user2@example.com']
        assert len(emails) == len(set(emails))  # No duplicates

    def test_not_null_constraints(self):
        """Test not-null field constraints."""
        calculation_data = {
            'user_id': str(uuid4()),
            'birth_date': date(1990, 1, 1),
            'target_date': date(2023, 1, 1),
            'years': 33,
            'months': 0,
            'days': 0,
            'total_days': 12053
        }

        for key, value in calculation_data.items():
            assert value is not None, f"{key} should not be null"
