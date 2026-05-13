from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from datetime import datetime, date
from pydantic import BaseModel

from app.services.calculation_engine import CalculationEngine
from app.services.validation_service import ValidationService
from app.services.report_service import ReportService

router = APIRouter()

# Initialize services with integration
validation_service = ValidationService()
calculation_engine = CalculationEngine(validation_service=validation_service)
report_service = ReportService(calculation_engine=calculation_engine)

class AgeCalculationRequest(BaseModel):
    birth_date: str
    target_date: str = None
    include_analytics: bool = True

class BulkCalculationRequest(BaseModel):
    calculations: List[AgeCalculationRequest]

@router.post("/calculate")
async def calculate_age(request: AgeCalculationRequest) -> Dict[str, Any]:
    """Calculate age with analytics and validation"""
    try:
        # Service integration: validation -> calculation -> analytics
        result = calculation_engine.calculate_age_with_analytics(
            birth_date=request.birth_date,
            target_date=request.target_date,
            include_analytics=request.include_analytics
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}")

@router.post("/calculate/bulk")
async def calculate_bulk_ages(request: BulkCalculationRequest) -> Dict[str, Any]:
    """Calculate multiple ages with batch processing"""
    try:
        results = []
        for calc_request in request.calculations:
            result = calculation_engine.calculate_age_with_analytics(
                birth_date=calc_request.birth_date,
                target_date=calc_request.target_date,
                include_analytics=calc_request.include_analytics
            )
            results.append(result)

        return {
            "results": results,
            "total_processed": len(results),
            "summary": calculation_engine.get_batch_analytics(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk calculation failed: {str(e)}")

@router.get("/analytics/{birth_date}")
async def get_age_analytics(birth_date: str) -> Dict[str, Any]:
    """Get detailed analytics for a specific birth date"""
    try:
        analytics = calculation_engine.get_detailed_analytics(birth_date)
        return analytics
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics failed: {str(e)}")

@router.post("/report")
async def generate_report(request: Dict[str, Any]) -> Dict[str, Any]:
    """Generate age calculation report"""
    try:
        report = report_service.generate_calculation_report(request)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")
