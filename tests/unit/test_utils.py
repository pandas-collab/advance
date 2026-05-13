"""Unit tests for utility functions."""
import pytest
from datetime import datetime, date
from unittest.mock import Mock, patch

class TestDateUtils:
    """Test cases for date utility functions."""

    def test_parse_date_string(self):
        """Test date string parsing."""
        def parse_date_string(date_str):
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return None

        valid_dates = ['2023-01-01', '1990-12-31', '2000-02-29']
        invalid_dates = ['2023-13-01', '1990-02-30', 'invalid-date']

        for date_str in valid_dates:
            result = parse_date_string(date_str)
            assert result is not None
            assert isinstance(result, date)

        for date_str in invalid_dates:
            result = parse_date_string(date_str)
            assert result is None

    def test_format_age_string(self):
        """Test age formatting utility."""
        def format_age_string(years, months, days):
            parts = []
            if years > 0:
                parts.append(f"{years} year{'s' if years != 1 else ''}")
            if months > 0:
                parts.append(f"{months} month{'s' if months != 1 else ''}")
            if days > 0:
                parts.append(f"{days} day{'s' if days != 1 else ''}")
            return ', '.join(parts) if parts else '0 days'

        test_cases = [
            (1, 0, 0, '1 year'),
            (2, 1, 1, '2 years, 1 month, 1 day'),
            (0, 0, 5, '5 days'),
            (0, 0, 0, '0 days')
        ]

        for years, months, days, expected in test_cases:
            result = format_age_string(years, months, days)
            assert result == expected

class TestValidationUtils:
    """Test cases for validation utilities."""

    def test_validate_email(self):
        """Test email validation utility."""
        import re

        def validate_email(email):
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return re.match(pattern, email) is not None

        valid_emails = [
            'user@example.com',
            'test.email+tag@domain.org',
            'admin@sub.domain.co.uk'
        ]

        invalid_emails = [
            'invalid-email',
            '@example.com',
            'user@',
            'user@domain',
            ''
        ]

        for email in valid_emails:
            assert validate_email(email) is True

        for email in invalid_emails:
            assert validate_email(email) is False

    def test_sanitize_input(self):
        """Test input sanitization utility."""
        def sanitize_input(text):
            if not isinstance(text, str):
                return ''
            # Remove potential XSS characters
            dangerous_chars = ['<', '>', '&', '"', "'", '`']
            sanitized = text
            for char in dangerous_chars:
                sanitized = sanitized.replace(char, '')
            return sanitized.strip()

        test_cases = [
            ('<script>alert("xss")</script>', 'scriptalert("xss")/script'),
            ('Normal text', 'Normal text'),
            ('  spaced  ', 'spaced'),
            ('', ''),
            (None, '')
        ]

        for input_text, expected in test_cases:
            result = sanitize_input(input_text)
            assert result == expected

class TestResponseUtils:
    """Test cases for API response utilities."""

    def test_format_api_response(self):
        """Test API response formatting."""
        def format_api_response(data=None, message=None, status='success'):
            response = {'status': status}
            if data is not None:
                response['data'] = data
            if message:
                response['message'] = message
            return response

        # Test success response with data
        response = format_api_response({'user_id': '123'}, 'User created')
        assert response['status'] == 'success'
        assert response['data']['user_id'] == '123'
        assert response['message'] == 'User created'

        # Test error response
        error_response = format_api_response(message='Validation error', status='error')
        assert error_response['status'] == 'error'
        assert error_response['message'] == 'Validation error'
        assert 'data' not in error_response

    def test_pagination_utils(self):
        """Test pagination utility functions."""
        def calculate_pagination(total_items, page_size, current_page):
            total_pages = (total_items + page_size - 1) // page_size
            offset = (current_page - 1) * page_size

            return {
                'total_items': total_items,
                'total_pages': total_pages,
                'current_page': current_page,
                'page_size': page_size,
                'offset': offset,
                'has_next': current_page < total_pages,
                'has_prev': current_page > 1
            }

        pagination = calculate_pagination(100, 10, 3)

        assert pagination['total_pages'] == 10
        assert pagination['offset'] == 20
        assert pagination['has_next'] is True
        assert pagination['has_prev'] is True
