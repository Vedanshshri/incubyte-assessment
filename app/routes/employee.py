from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.database import get_db

router = APIRouter()

@router.post('', response_model=EmployeeResponse, status_code=201)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Create a new employee"""
    db_employee = Employee(
        full_name=employee.full_name,
        job_title=employee.job_title,
        country=employee.country,
        salary=employee.salary
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get('', response_model=list[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db)):
    """Get all employees"""
    employees = db.query(Employee).all()
    return employees

@router.get('/{employee_id}', response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get a specific employee"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail='Employee not found')
    return employee

@router.put('/{employee_id}', response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    """Update an employee"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail='Employee not found')
    
    update_data = employee_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)
    
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@router.delete('/{employee_id}')
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Delete an employee"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail='Employee not found')
    
    db.delete(employee)
    db.commit()
    return {'message': 'Employee deleted successfully'}
