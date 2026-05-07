from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Employee
from app.schemas import SalaryCalculationRequest, SalaryCalculationResponse, CountrySalaryMetrics, JobTitleSalaryMetrics
from app.database import get_db

router = APIRouter()

DEDUCTION_RATES = {
    'India': 0.10,
    'United States': 0.12
}

def calculate_salary_deductions(employee_id: int, gross_salary: float, db: Session):
    """Calculate deductions and net salary for an employee"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        return None
    
    country = employee.country
    deduction_rate = DEDUCTION_RATES.get(country, 0.0)
    deductions = gross_salary * deduction_rate
    net_salary = gross_salary - deductions
    
    return {
        'employee_id': employee_id,
        'gross_salary': gross_salary,
        'country': country,
        'deduction_rate': deduction_rate * 100,
        'deductions': round(deductions, 2),
        'net_salary': round(net_salary, 2)
    }

@router.post('/calculate/{employee_id}', response_model=SalaryCalculationResponse)
def calculate_salary(
    employee_id: int,
    request: SalaryCalculationRequest,
    db: Session = Depends(get_db)
):
    """Calculate salary deductions for an employee"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail='Employee not found')
    
    result = calculate_salary_deductions(employee_id, request.gross_salary, db)
    if result is None:
        raise HTTPException(status_code=404, detail='Employee not found')
    return result

@router.get('/metrics/country/{country}', response_model=CountrySalaryMetrics)
def get_country_salary_metrics(country: str, db: Session = Depends(get_db)):
    """Get min, max, and average salary for a country"""
    employees = db.query(Employee).filter(Employee.country == country).all()
    
    if not employees:
        raise HTTPException(status_code=404, detail=f'No employees found in {country}')
    
    salaries = [emp.salary for emp in employees]
    
    return {
        'country': country,
        'count': len(salaries),
        'minimum_salary': min(salaries),
        'maximum_salary': max(salaries),
        'average_salary': round(sum(salaries) / len(salaries), 2)
    }

@router.get('/metrics/job-title/{job_title}', response_model=JobTitleSalaryMetrics)
def get_job_title_salary_metrics(job_title: str, db: Session = Depends(get_db)):
    """Get average salary for a specific job title"""
    employees = db.query(Employee).filter(Employee.job_title == job_title).all()
    
    if not employees:
        raise HTTPException(status_code=404, detail=f'No employees found with job title: {job_title}')
    
    salaries = [emp.salary for emp in employees]
    
    return {
        'job_title': job_title,
        'count': len(salaries),
        'average_salary': round(sum(salaries) / len(salaries), 2)
    }
