"""Entry point for FastAPI application"""
from fastapi import FastAPI
from app.routes import employee, salary
from app.database import engine
from app.models import Base

# Create tables on startup
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title='Salary Management API',
    description='API for managing employee salaries with deductions and metrics',
    version='1.0.0'
)

app.include_router(employee.router, prefix='/api/employees', tags=['employees'])
app.include_router(salary.router, prefix='/api/salary', tags=['salary'])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
