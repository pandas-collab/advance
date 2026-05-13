from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Advanced Age Calculator API",
    description="FastAPI backend for age calculation with authentication",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Advanced Age Calculator API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/v1/calculate-age")
async def calculate_age(birth_date: str):
    from datetime import datetime, date
    try:
        birth = datetime.strptime(birth_date, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return {
            "birth_date": birth_date,
            "current_age": age,
            "days_lived": (today - birth).days
        }
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}
