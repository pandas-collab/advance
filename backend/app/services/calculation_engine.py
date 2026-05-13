from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
import calendar
from dateutil.relativedelta import relativedelta

class CalculationEngine:
    """Advanced age calculation engine with analytics"""

    def __init__(self, validation_service=None):
        """Initialize with optional validation service integration"""
        self.validation_service = validation_service
        self.calculation_history = []

    def calculate_age_with_analytics(self, birth_date: str, target_date: str = None,
                                   include_analytics: bool = True) -> Dict[str, Any]:
        """
        Calculate age with comprehensive analytics and validation
        Integrates with validation service for input validation
        """
        # Service integration: use validation service if available
        if self.validation_service:
            validation_result = self.validation_service.validate_date_inputs(birth_date, target_date)
            if not validation_result["is_valid"]:
                raise ValueError(f"Validation failed: {validation_result['errors']}")

        # Parse dates
        birth_dt = self._parse_date(birth_date)
        target_dt = self._parse_date(target_date) if target_date else datetime.now().date()

        # Basic age calculation
        age_result = self._calculate_precise_age(birth_dt, target_dt)

        result = {
            "basic_age": age_result,
            "calculation_timestamp": datetime.now().isoformat(),
            "input_validation": validation_result if self.validation_service else {"status": "skipped"}
        }

        # Add analytics if requested
        if include_analytics:
            result["analytics"] = self._generate_analytics(birth_dt, target_dt)

        # Store in history for batch analytics
        self.calculation_history.append(result)

        return result

    def _calculate_precise_age(self, birth_date: date, target_date: date) -> Dict[str, Any]:
        """Calculate precise age with multiple formats"""
        if birth_date > target_date:
            raise ValueError("Birth date cannot be in the future")

        # Calculate using relativedelta for precise month/year calculation
        age_delta = relativedelta(target_date, birth_date)

        # Total days calculation
        total_days = (target_date - birth_date).days

        return {
            "years": age_delta.years,
            "months": age_delta.months,
            "days": age_delta.days,
            "total_days": total_days,
            "total_weeks": total_days // 7,
            "total_months": age_delta.years * 12 + age_delta.months,
            "formatted": f"{age_delta.years} years, {age_delta.months} months, {age_delta.days} days"
        }

    def _generate_analytics(self, birth_date: date, target_date: date) -> Dict[str, Any]:
        """Generate comprehensive analytics"""
        age_delta = relativedelta(target_date, birth_date)
        total_days = (target_date - birth_date).days

        # Calculate next birthday
        next_birthday = date(target_date.year, birth_date.month, birth_date.day)
        if next_birthday <= target_date:
            next_birthday = date(target_date.year + 1, birth_date.month, birth_date.day)

        days_to_birthday = (next_birthday - target_date).days

        # Life stage analysis
        life_stage = self._determine_life_stage(age_delta.years)

        # Zodiac and birth info
        zodiac_sign = self._get_zodiac_sign(birth_date.month, birth_date.day)
        day_of_week = birth_date.strftime("%A")

        return {
            "life_stage": life_stage,
            "next_birthday": {
                "date": next_birthday.isoformat(),
                "days_until": days_to_birthday,
                "day_of_week": next_birthday.strftime("%A")
            },
            "birth_info": {
                "zodiac_sign": zodiac_sign,
                "birth_day_of_week": day_of_week,
                "birth_month_name": birth_date.strftime("%B")
            },
            "milestones": self._calculate_milestones(birth_date, target_date),
            "statistics": {
                "approximate_heartbeats": total_days * 100000,  # Rough estimate
                "approximate_breaths": total_days * 20000,      # Rough estimate
                "seasons_lived": total_days // 91,              # Approximate seasons
            }
        }

    def get_detailed_analytics(self, birth_date: str) -> Dict[str, Any]:
        """Get detailed analytics for a birth date"""
        birth_dt = self._parse_date(birth_date)
        target_dt = datetime.now().date()

        # Service integration for validation
        if self.validation_service:
            validation_result = self.validation_service.validate_date_inputs(birth_date, None)
            if not validation_result["is_valid"]:
                raise ValueError(f"Invalid birth date: {validation_result['errors']}")

        return self._generate_analytics(birth_dt, target_dt)

    def get_batch_analytics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate analytics for batch calculations"""
        if not results:
            return {"message": "No calculations to analyze"}

        ages = [r["basic_age"]["years"] for r in results if "basic_age" in r]

        return {
            "total_calculations": len(results),
            "age_statistics": {
                "average_age": sum(ages) / len(ages) if ages else 0,
                "min_age": min(ages) if ages else 0,
                "max_age": max(ages) if ages else 0
            },
            "processing_summary": {
                "successful": len(results),
                "with_analytics": len([r for r in results if "analytics" in r])
            }
        }

    def _parse_date(self, date_str: str) -> date:
        """Parse date string to date object"""
        if not date_str:
            return datetime.now().date()

        # Try common date formats
        formats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"]

        for fmt in formats:
            try:
                parsed_dt = datetime.strptime(date_str, fmt)
                return parsed_dt.date()
            except ValueError:
                continue

        raise ValueError(f"Unable to parse date: {date_str}")

    def _determine_life_stage(self, years: int) -> str:
        """Determine life stage based on age"""
        if years < 2:
            return "Infant"
        elif years < 13:
            return "Child"
        elif years < 20:
            return "Teenager"
        elif years < 40:
            return "Young Adult"
        elif years < 65:
            return "Adult"
        else:
            return "Senior"

    def _get_zodiac_sign(self, month: int, day: int) -> str:
        """Get zodiac sign based on birth date"""
        zodiac_dates = [
            (1, 20, "Capricorn"), (2, 19, "Aquarius"), (3, 21, "Pisces"),
            (4, 20, "Aries"), (5, 21, "Taurus"), (6, 21, "Gemini"),
            (7, 23, "Cancer"), (8, 23, "Leo"), (9, 23, "Virgo"),
            (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius")
        ]

        for i, (end_month, end_day, sign) in enumerate(zodiac_dates):
            if month < end_month or (month == end_month and day <= end_day):
                return sign

        return "Capricorn"  # Default for late December

    def _calculate_milestones(self, birth_date: date, target_date: date) -> Dict[str, Any]:
        """Calculate important age milestones"""
        age_years = relativedelta(target_date, birth_date).years

        milestones_passed = []
        upcoming_milestones = []

        milestone_ages = [1, 5, 10, 13, 16, 18, 21, 25, 30, 40, 50, 65, 75, 100]

        for milestone in milestone_ages:
            if age_years >= milestone:
                milestone_date = date(birth_date.year + milestone, birth_date.month, birth_date.day)
                milestones_passed.append({
                    "age": milestone,
                    "date_reached": milestone_date.isoformat()
                })
            elif len(upcoming_milestones) < 3:  # Show next 3 milestones
                milestone_date = date(birth_date.year + milestone, birth_date.month, birth_date.day)
                days_until = (milestone_date - target_date).days
                upcoming_milestones.append({
                    "age": milestone,
                    "date": milestone_date.isoformat(),
                    "days_until": days_until
                })

        return {
            "milestones_passed": milestones_passed[-5:],  # Last 5 milestones
            "upcoming_milestones": upcoming_milestones
        }
