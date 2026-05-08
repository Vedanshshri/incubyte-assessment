from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class EmployeeCreate(BaseModel):
    """Schema for creating an employee"""
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    full_name: str = Field(min_length=1)
    job_title: str = Field(min_length=1)
    country: str = Field(min_length=1)
    salary: float = Field(gt=0, description="Salary must be a positive number")

class EmployeeUpdate(BaseModel):
    """Schema for updating an employee"""
    model_config = ConfigDict(str_strip_whitespace=True)

    full_name: Optional[str] = Field(None, min_length=1)
    job_title: Optional[str] = Field(None, min_length=1)
    country: Optional[str] = Field(None, min_length=1)
    salary: Optional[float] = Field(None, gt=0, description="Salary must be a positive number")

class EmployeeResponse(BaseModel):
    """Schema for employee response"""
    id: int
    full_name: str
    job_title: str
    country: str
    salary: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class SalaryCalculationResponse(BaseModel):
    """Schema for salary calculation response"""
    employee_id: int
    gross_salary: float
    country: str
    deduction_rate: float
    deductions: float
    net_salary: float

class CountrySalaryMetrics(BaseModel):
    """Schema for country salary metrics"""
    country: str
    count: int
    minimum_salary: float
    maximum_salary: float
    average_salary: float

class JobTitleSalaryMetrics(BaseModel):
    """Schema for job title salary metrics"""
    job_title: str
    count: int
    average_salary: float
