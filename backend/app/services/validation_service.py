from datetime import datetime, date
from typing import Dict, Any, List
import re

class ValidationService:
    """Validation service for age calculation inputs"""

    def __init__(self):
        self.validation_rules = {
            "date_format_patterns": [
                r"^\d{4}-\d{2}-\d{2}$",  # YYYY-MM-DD
                r"^\d{2}/\d{2}/\d{4}$",  # MM/DD/YYYY
                r"^\d{2}/\d{2}/\d{4}$",  # DD/MM/YYYY
            ],
            "min_year": 1900,
            "max_year": datetime.now().year + 1
        }

    def validate_date_inputs(self, birth_date: str, target_date: str = None) -> Dict[str, Any]:
        """
        Validate date inputs for calculation engine integration
        Returns standardized validation result
        """
        errors = []
        warnings = []

        # Validate birth date
        birth_validation = self._validate_single_date(birth_date, "birth_date")
        if not birth_validation["is_valid"]:
            errors.extend(birth_validation["errors"])

        # Validate target date if provided
        if target_date:
            target_validation = self._validate_single_date(target_date, "target_date")
            if not target_validation["is_valid"]:
                errors.extend(target_validation["errors"])
            else:
                # Check date logic
                try:
                    birth_dt = self._parse_date_safely(birth_date)
                    target_dt = self._parse_date_safely(target_date)
                    if birth_dt and target_dt and birth_dt > target_dt:
                        errors.append("Birth date cannot be after target date")
                except:
                    pass  # Already handled in individual validations

        # Check for future birth dates
        if birth_date:
            try:
                birth_dt = self._parse_date_safely(birth_date)
                if birth_dt and birth_dt > datetime.now().date():
                    warnings.append("Birth date is in the future")
            except:
                pass

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "validation_timestamp": datetime.now().isoformat()
        }

    def validate_calculation_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a complete calculation request"""
        errors = []

        # Check required fields
        if "birth_date" not in request_data:
            errors.append("birth_date is required")

        # Validate dates if present
        if "birth_date" in request_data:
            date_validation = self.validate_date_inputs(
                request_data["birth_date"],
                request_data.get("target_date")
            )
            if not date_validation["is_valid"]:
                errors.extend(date_validation["errors"])

        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }

    def validate_bulk_request(self, calculations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate bulk calculation request"""
        errors = []
        valid_count = 0

        if not calculations:
            errors.append("No calculations provided")
        elif len(calculations) > 100:  # Arbitrary limit
            errors.append("Too many calculations (max 100)")
        else:
            for i, calc in enumerate(calculations):
                calc_validation = self.validate_calculation_request(calc)
                if calc_validation["is_valid"]:
                    valid_count += 1
                else:
                    errors.append(f"Calculation {i+1}: {', '.join(calc_validation['errors'])}")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "valid_calculations": valid_count,
            "total_calculations": len(calculations) if calculations else 0
        }

    def _validate_single_date(self, date_str: str, field_name: str) -> Dict[str, Any]:
        """Validate a single date string"""
        errors = []

        if not date_str:
            errors.append(f"{field_name} cannot be empty")
            return {"is_valid": False, "errors": errors}

        # Check format
        format_valid = False
        for pattern in self.validation_rules["date_format_patterns"]:
            if re.match(pattern, date_str.strip()):
                format_valid = True
                break

        if not format_valid:
            errors.append(f"{field_name} format is invalid. Use YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY")
            return {"is_valid": False, "errors": errors}

        # Try to parse the date
        parsed_date = self._parse_date_safely(date_str)
        if not parsed_date:
            errors.append(f"{field_name} is not a valid date")
        else:
            # Check year bounds
            if parsed_date.year < self.validation_rules["min_year"]:
                errors.append(f"{field_name} year cannot be before {self.validation_rules['min_year']}")
            elif parsed_date.year > self.validation_rules["max_year"]:
                errors.append(f"{field_name} year cannot be after {self.validation_rules['max_year']}")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }

    def _parse_date_safely(self, date_str: str) -> date:
        """Safely parse date string without raising exceptions"""
        formats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"]

        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt).date()
            except ValueError:
                continue

        return None

    def get_validation_rules(self) -> Dict[str, Any]:
        """Get current validation rules for API documentation"""
        return {
            "supported_formats": [
                "YYYY-MM-DD (ISO format)",
                "MM/DD/YYYY (US format)",
                "DD/MM/YYYY (EU format)"
            ],
            "year_range": {
                "min": self.validation_rules["min_year"],
                "max": self.validation_rules["max_year"]
            },
            "rules": [
                "Birth date cannot be in the future",
                "Birth date cannot be after target date",
                "All dates must be valid calendar dates"
            ]
        }
