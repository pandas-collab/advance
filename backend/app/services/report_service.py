"""
Report Service
Handles report generation for age calculations.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, date
import json


class ReportService:
    """Service for generating various types of age calculation reports."""

    def __init__(self):
        """Initialize the report service."""
        self.report_templates = {}

    def generate_age_report(self, calculation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive age report.

        Args:
            calculation_data: Dictionary containing age calculation results

        Returns:
            Dictionary containing formatted report data
        """
        try:
            report = {
                "report_id": f"age_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "generated_at": datetime.now().isoformat(),
                "calculation_data": calculation_data,
                "summary": self._generate_summary(calculation_data),
                "analytics": self._generate_analytics(calculation_data)
            }
            return report
        except Exception as e:
            return {"error": f"Failed to generate report: {str(e)}"}

    def generate_batch_report(self, calculations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a batch report for multiple calculations.

        Args:
            calculations: List of calculation results

        Returns:
            Dictionary containing batch report data
        """
        try:
            report = {
                "report_id": f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "generated_at": datetime.now().isoformat(),
                "total_calculations": len(calculations),
                "calculations": calculations,
                "batch_analytics": self._generate_batch_analytics(calculations)
            }
            return report
        except Exception as e:
            return {"error": f"Failed to generate batch report: {str(e)}"}

    def export_report(self, report_data: Dict[str, Any], format_type: str = "json") -> str:
        """
        Export report in specified format.

        Args:
            report_data: Report data to export
            format_type: Export format (json, csv, etc.)

        Returns:
            Formatted report string
        """
        try:
            if format_type.lower() == "json":
                return json.dumps(report_data, indent=2, default=str)
            elif format_type.lower() == "csv":
                return self._convert_to_csv(report_data)
            else:
                return json.dumps(report_data, indent=2, default=str)
        except Exception as e:
            return f"Export error: {str(e)}"

    def _generate_summary(self, calculation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary section for report."""
        return {
            "birth_date": calculation_data.get("birth_date", ""),
            "current_age": calculation_data.get("current_age", {}),
            "calculation_type": calculation_data.get("calculation_type", "standard")
        }

    def _generate_analytics(self, calculation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate analytics section for report."""
        return {
            "age_milestones": calculation_data.get("milestones", []),
            "statistical_data": calculation_data.get("statistics", {}),
            "trends": []
        }

    def _generate_batch_analytics(self, calculations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate analytics for batch calculations."""
        if not calculations:
            return {}

        return {
            "average_age": self._calculate_average_age(calculations),
            "age_distribution": self._calculate_age_distribution(calculations),
            "common_birth_years": self._find_common_birth_years(calculations)
        }

    def _calculate_average_age(self, calculations: List[Dict[str, Any]]) -> float:
        """Calculate average age from calculations."""
        try:
            ages = []
            for calc in calculations:
                age_data = calc.get("current_age", {})
                if "years" in age_data:
                    ages.append(float(age_data["years"]))
            return sum(ages) / len(ages) if ages else 0.0
        except Exception:
            return 0.0

    def _calculate_age_distribution(self, calculations: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate age distribution ranges."""
        distribution = {"0-18": 0, "19-30": 0, "31-50": 0, "51-70": 0, "70+": 0}

        try:
            for calc in calculations:
                age_data = calc.get("current_age", {})
                if "years" in age_data:
                    age = int(age_data["years"])
                    if age <= 18:
                        distribution["0-18"] += 1
                    elif age <= 30:
                        distribution["19-30"] += 1
                    elif age <= 50:
                        distribution["31-50"] += 1
                    elif age <= 70:
                        distribution["51-70"] += 1
                    else:
                        distribution["70+"] += 1
        except Exception:
            pass

        return distribution

    def _find_common_birth_years(self, calculations: List[Dict[str, Any]]) -> List[int]:
        """Find most common birth years."""
        try:
            birth_years = []
            for calc in calculations:
                birth_date = calc.get("birth_date", "")
                if birth_date:
                    year = datetime.fromisoformat(birth_date.replace('Z', '+00:00')).year
                    birth_years.append(year)

            # Count occurrences and return top 5
            year_counts = {}
            for year in birth_years:
                year_counts[year] = year_counts.get(year, 0) + 1

            return sorted(year_counts.keys(), key=lambda x: year_counts[x], reverse=True)[:5]
        except Exception:
            return []

    def _convert_to_csv(self, report_data: Dict[str, Any]) -> str:
        """Convert report data to CSV format."""
        try:
            lines = ["Report ID,Generated At,Type,Value"]
            report_id = report_data.get("report_id", "")
            generated_at = report_data.get("generated_at", "")

            for key, value in report_data.items():
                if key not in ["report_id", "generated_at"]:
                    lines.append(f"{report_id},{generated_at},{key},{str(value)}")

            return "\n".join(lines)
        except Exception as e:
            return f"CSV conversion error: {str(e)}"
