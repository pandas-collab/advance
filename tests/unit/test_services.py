"""Unit tests for service layer components."""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, date
import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from backend.app.services.calculation_engine import CalculationEngine
from backend.app.services.validation_service import ValidationService
from backend.app.services.report_service import ReportService

class TestCalculationEngine:
    """Test cases for CalculationEngine service."""

    def setup_method(self):
        """Setup test fixtures."""
        self.engine = CalculationEngine()

    def test_calculate_age_basic(self):
        """Test basic age calculation."""
        birth_date = date(1990, 1, 1)
        target_date = date(2023, 1, 1)

        result = self.engine.calculate_age(birth_date, target_date)

        assert result['years'] == 33
        assert result['months'] == 0
        assert result['days'] == 0
        assert result['total_days'] == 12053

    def test_calculate_age_leap_year(self):
        """Test age calculation with leap year."""
        birth_date = date(2000, 2, 29)
        target_date = date(2024, 2, 29)

        result = self.engine.calculate_age(birth_date, target_date)

        assert result['years'] == 24
        assert result['months'] == 0
        assert result['days'] == 0

    def test_calculate_age_invalid_dates(self):
        """Test age calculation with invalid dates."""
        birth_date = date(2023, 1, 1)
        target_date = date(1990, 1, 1)

        with pytest.raises(ValueError):
            self.engine.calculate_age(birth_date, target_date)

    def test_calculate_age_precision_days(self):
        """Test age calculation with day precision."""
        birth_date = date(1990, 5, 15)
        target_date = date(2023, 8, 22)

        result = self.engine.calculate_age(birth_date, target_date, precision="days")

        assert result['years'] == 33
        assert result['months'] == 3
        assert result['days'] == 7

class TestValidationService:
    """Test cases for ValidationService."""

    def setup_method(self):
        """Setup test fixtures."""
        self.service = ValidationService()

    def test_validate_birth_date_valid(self):
        """Test valid birth date validation."""
        birth_date = date(1990, 1, 1)

        result = self.service.validate_birth_date(birth_date)

        assert result is True

    def test_validate_birth_date_future(self):
        """Test future birth date validation."""
        future_date = date(2030, 1, 1)

        with pytest.raises(ValueError, match="Birth date cannot be in the future"):
            self.service.validate_birth_date(future_date)

    def test_validate_date_range_valid(self):
        """Test valid date range validation."""
        birth_date = date(1990, 1, 1)
        target_date = date(2023, 1, 1)

        result = self.service.validate_date_range(birth_date, target_date)

        assert result is True

    def test_validate_date_range_invalid(self):
        """Test invalid date range validation."""
        birth_date = date(2023, 1, 1)
        target_date = date(1990, 1, 1)

        with pytest.raises(ValueError, match="Target date must be after birth date"):
            self.service.validate_date_range(birth_date, target_date)

    @patch('backend.app.services.validation_service.ValidationService.get_validation_rules')
    def test_apply_validation_rules(self, mock_get_rules):
        """Test applying validation rules."""
        mock_get_rules.return_value = [
            {"name": "min_age", "config": {"min_years": 0}},
            {"name": "max_age", "config": {"max_years": 150}}
        ]

        birth_date = date(1990, 1, 1)
        target_date = date(2023, 1, 1)

        result = self.service.apply_validation_rules(birth_date, target_date)

        assert result is True

class TestReportService:
    """Test cases for ReportService."""

    def setup_method(self):
        """Setup test fixtures."""
        self.service = ReportService()

    @pytest.mark.asyncio
    async def test_generate_calculation_report(self):
        """Test calculation report generation."""
        calculation_data = {
            'calculation_id': 'test-123',
            'birth_date': '1990-01-01',
            'target_date': '2023-01-01',
            'years': 33,
            'months': 0,
            'days': 0,
            'total_days': 12053
        }

        report = await self.service.generate_calculation_report(calculation_data)

        assert 'summary' in report
        assert 'details' in report
        assert report['summary']['age_years'] == 33

    @pytest.mark.asyncio
    async def test_generate_user_analytics(self):
        """Test user analytics generation."""
        user_id = 'user-123'

        with patch.object(self.service, 'get_user_calculations') as mock_get:
            mock_get.return_value = [
                {'years': 25, 'created_at': '2023-01-01'},
                {'years': 30, 'created_at': '2023-02-01'}
            ]

            analytics = await self.service.generate_user_analytics(user_id)

            assert 'total_calculations' in analytics
            assert 'average_age' in analytics
            assert analytics['total_calculations'] == 2

    def test_format_age_display(self):
        """Test age display formatting."""
        age_data = {'years': 33, 'months': 6, 'days': 15}

        formatted = self.service.format_age_display(age_data)

        assert '33 years' in formatted
        assert '6 months' in formatted
        assert '15 days' in formatted
