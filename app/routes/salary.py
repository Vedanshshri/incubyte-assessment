from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.models import Employee
from app.schemas import SalaryCalculationResponse
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

@router.get('/calculate/{employee_id}', response_model=SalaryCalculationResponse)
def calculate_salary(
    employee_id: int,
    gross_salary: float = Query(gt=0, description="Gross salary must be a positive number"),
    db: Session = Depends(get_db)
):
    """Calculate salary deductions for an employee"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail='Employee not found')
    
    result = calculate_salary_deductions(employee_id, gross_salary, db)
    if result is None:
        raise HTTPException(status_code=404, detail='Employee not found')
    return result
