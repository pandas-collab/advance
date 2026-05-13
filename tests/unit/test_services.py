"""Unit tests for service layer functionality."""
import pytest
from datetime import datetime, date
from unittest.mock import Mock, patch
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

from backend.app.services.calculation_engine import AgeCalculationEngine
from backend.app.services.validation_service import ValidationService
from backend.app.services.report_service import ReportService

class TestAgeCalculationEngine:
    """Test cases for age calculation engine."""

    def setup_method(self):
        """Setup test fixtures."""
        self.calculator = AgeCalculationEngine()

    def test_calculate_age_basic(self):
        """Test basic age calculation."""
        birth_date = date(1990, 1, 1)
        target_date = date(2023, 1, 1)

        result = self.calculator.calculate_age(birth_date, target_date)

        assert result['years'] == 33
        assert result['months'] == 0
        assert result['days'] == 0
        assert result['total_days'] == 12053

    def test_calculate_age_with_months_days(self):
        """Test age calculation with partial months and days."""
        birth_date = date(1990, 3, 15)
        target_date = date(2023, 7, 22)

        result = self.calculator.calculate_age(birth_date, target_date)

        assert result['years'] == 33
        assert result['months'] == 4
        assert result['days'] == 7

    def test_leap_year_handling(self):
        """Test leap year calculations."""
        birth_date = date(2000, 2, 29)  # Leap year
        target_date = date(2001, 2, 28)

        result = self.calculator.calculate_age(birth_date, target_date)

        assert result['years'] == 0
        assert result['months'] == 11
        assert result['days'] == 30

    def test_invalid_date_range(self):
        """Test handling of invalid date ranges."""
        birth_date = date(2023, 1, 1)
        target_date = date(2020, 1, 1)  # Target before birth

        with pytest.raises(ValueError, match="Target date must be after birth date"):
            self.calculator.calculate_age(birth_date, target_date)

class TestValidationService:
    """Test cases for validation service."""

    def setup_method(self):
        """Setup test fixtures."""
        self.validator = ValidationService()

    def test_validate_date_format(self):
        """Test date format validation."""
        valid_date = "1990-01-01"
        invalid_date = "01-01-1990"

        assert self.validator.validate_date_format(valid_date) is True
        assert self.validator.validate_date_format(invalid_date) is False

    def test_validate_date_range(self):
        """Test date range validation."""
        birth_date = date(1990, 1, 1)
        valid_target = date(2023, 1, 1)
        invalid_target = date(1989, 1, 1)

        assert self.validator.validate_date_range(birth_date, valid_target) is True
        assert self.validator.validate_date_range(birth_date, invalid_target) is False

    def test_validate_precision_level(self):
        """Test precision level validation."""
        valid_levels = ["days", "months", "years"]
        invalid_level = "hours"

        for level in valid_levels:
            assert self.validator.validate_precision_level(level) is True

        assert self.validator.validate_precision_level(invalid_level) is False

class TestReportService:
    """Test cases for report service."""

    def setup_method(self):
        """Setup test fixtures."""
        self.report_service = ReportService()

    @patch('backend.app.services.report_service.ReportService.get_calculation_history')
    def test_generate_user_report(self, mock_history):
        """Test user report generation."""
        mock_history.return_value = [
            {
                'calculation_id': '123',
                'birth_date': '1990-01-01',
                'target_date': '2023-01-01',
                'years': 33,
                'created_at': '2023-01-01T00:00:00'
            }
        ]

        report = self.report_service.generate_user_report('user123')

        assert 'total_calculations' in report
        assert 'calculations' in report
        assert report['total_calculations'] == 1

    def test_format_calculation_result(self):
        """Test calculation result formatting."""
        raw_result = {
            'years': 33,
            'months': 4,
            'days': 7,
            'total_days': 12153
        }

        formatted = self.report_service.format_calculation_result(raw_result)

        assert 'age_string' in formatted
        assert '33 years, 4 months, 7 days' in formatted['age_string']
