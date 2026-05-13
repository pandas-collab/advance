"""Unit tests for utility functions."""
import pytest
from datetime import datetime, date, timedelta
from uuid import UUID
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

class TestDateUtils:
    """Test cases for date utility functions."""

    def test_date_string_parsing(self):
        """Test date string parsing."""
        date_string = "1990-01-01"
        parsed_date = datetime.strptime(date_string, "%Y-%m-%d").date()

        assert parsed_date == date(1990, 1, 1)
        assert isinstance(parsed_date, date)

    def test_date_formatting(self):
        """Test date formatting."""
        test_date = date(1990, 1, 1)
        formatted = test_date.strftime("%Y-%m-%d")

        assert formatted == "1990-01-01"
        assert isinstance(formatted, str)

    def test_date_validation(self):
        """Test date validation utility."""
        def is_valid_date_string(date_str):
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return True
            except ValueError:
                return False

        assert is_valid_date_string("1990-01-01") is True
        assert is_valid_date_string("1990-13-01") is False
        assert is_valid_date_string("invalid-date") is False

    def test_date_range_validation(self):
        """Test date range validation."""
        def validate_date_range(start_date, end_date):
            if start_date >= end_date:
                raise ValueError("Start date must be before end date")
            return True

        # Valid range
        start = date(1990, 1, 1)
        end = date(2023, 1, 1)
        assert validate_date_range(start, end) is True

        # Invalid range
        with pytest.raises(ValueError):
            validate_date_range(end, start)

    def test_age_calculation_days(self):
        """Test age calculation in days."""
        birth_date = date(1990, 1, 1)
        target_date = date(1990, 1, 31)

        days_diff = (target_date - birth_date).days
        assert days_diff == 30

    def test_leap_year_detection(self):
        """Test leap year detection utility."""
        def is_leap_year(year):
            return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

        assert is_leap_year(2000) is True  # Divisible by 400
        assert is_leap_year(2004) is True  # Divisible by 4
        assert is_leap_year(1900) is False  # Divisible by 100 but not 400
        assert is_leap_year(2001) is False  # Not divisible by 4

class TestValidationUtils:
    """Test cases for validation utility functions."""

    def test_email_validation(self):
        """Test email validation utility."""
        def is_valid_email(email):
            import re
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return re.match(pattern, email) is not None

        assert is_valid_email("test@example.com") is True
        assert is_valid_email("user.name+tag@domain.co.uk") is True
        assert is_valid_email("invalid.email") is False
        assert is_valid_email("@example.com") is False
        assert is_valid_email("test@") is False

    def test_password_strength_validation(self):
        """Test password strength validation."""
        def validate_password_strength(password):
            if len(password) < 8:
                return False
            if not any(c.isupper() for c in password):
                return False
            if not any(c.islower() for c in password):
                return False
            if not any(c.isdigit() for c in password):
                return False
            return True

        assert validate_password_strength("StrongPass123") is True
        assert validate_password_strength("weak") is False
        assert validate_password_strength("NoNumbers") is False
        assert validate_password_strength("nonumbers123") is False

    def test_input_sanitization(self):
        """Test input sanitization utility."""
        def sanitize_input(text):
            if not isinstance(text, str):
                return str(text)
            # Remove potential XSS characters
            dangerous_chars = ['<', '>', '&', '"', "'"]
            sanitized = text
            for char in dangerous_chars:
                sanitized = sanitized.replace(char, '')
            return sanitized.strip()

        assert sanitize_input("Hello World") == "Hello World"
        assert sanitize_input("<script>alert('xss')</script>") == "scriptalert('xss')/script"
        assert sanitize_input("  test  ") == "test"

    def test_uuid_validation(self):
        """Test UUID validation utility."""
        def is_valid_uuid(uuid_string):
            try:
                UUID(uuid_string)
                return True
            except ValueError:
                return False

        valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
        invalid_uuid = "not-a-uuid"

        assert is_valid_uuid(valid_uuid) is True
        assert is_valid_uuid(invalid_uuid) is False

class TestResponseUtils:
    """Test cases for response formatting utilities."""

    def test_success_response_format(self):
        """Test success response formatting."""
        def format_success_response(data, message="Success"):
            return {
                "status": "success",
                "message": message,
                "data": data
            }

        data = {"user_id": "123", "email": "test@example.com"}
        response = format_success_response(data)

        assert response["status"] == "success"
        assert response["message"] == "Success"
        assert response["data"] == data

    def test_error_response_format(self):
        """Test error response formatting."""
        def format_error_response(message, error_code=None):
            response = {
                "status": "error",
                "message": message
            }
            if error_code:
                response["error_code"] = error_code
            return response

        response = format_error_response("Invalid input", "VALIDATION_ERROR")

        assert response["status"] == "error"
        assert response["message"] == "Invalid input"
        assert response["error_code"] == "VALIDATION_ERROR"

    def test_pagination_response_format(self):
        """Test pagination response formatting."""
        def format_paginated_response(data, page, per_page, total):
            return {
                "status": "success",
                "data": data,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                    "pages": (total + per_page - 1) // per_page
                }
            }

        data = [{"id": 1}, {"id": 2}]
        response = format_paginated_response(data, 1, 10, 25)

        assert response["pagination"]["page"] == 1
        assert response["pagination"]["per_page"] == 10
        assert response["pagination"]["total"] == 25
        assert response["pagination"]["pages"] == 3

class TestSecurityUtils:
    """Test cases for security utility functions."""

    def test_rate_limiting_check(self):
        """Test rate limiting utility."""
        def check_rate_limit(requests_count, time_window_seconds, limit):
            """Simple rate limiting check."""
            requests_per_second = requests_count / time_window_seconds
            return requests_per_second <= (limit / time_window_seconds)

        # Within limit
        assert check_rate_limit(10, 60, 100) is True  # 10 requests in 60 seconds, limit 100/60s

        # Exceeding limit
        assert check_rate_limit(200, 60, 100) is False  # 200 requests in 60 seconds, limit 100/60s

    def test_api_key_validation(self):
        """Test API key validation."""
        def validate_api_key_format(api_key):
            """Validate API key format."""
            if not isinstance(api_key, str):
                return False
            if len(api_key) < 32:
                return False
            # Check if contains only allowed characters
            allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            return all(c in allowed_chars for c in api_key)

        valid_key = "abcd1234567890ABCDEFGHIJKLmnopqr"
        invalid_key_short = "short"
        invalid_key_chars = "invalid-key-with-dash!"

        assert validate_api_key_format(valid_key) is True
        assert validate_api_key_format(invalid_key_short) is False
        assert validate_api_key_format(invalid_key_chars) is False

    def test_cors_validation(self):
        """Test CORS origin validation."""
        def is_allowed_origin(origin, allowed_origins):
            """Check if origin is in allowed list."""
            if not origin:
                return False
            return origin in allowed_origins

        allowed_origins = ["https://example.com", "https://app.example.com"]

        assert is_allowed_origin("https://example.com", allowed_origins) is True
        assert is_allowed_origin("https://malicious.com", allowed_origins) is False
        assert is_allowed_origin(None, allowed_origins) is False
