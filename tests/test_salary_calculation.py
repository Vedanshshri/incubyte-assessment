"""Test cases for salary calculation"""
import pytest

class TestSalaryCalculation:
    """Test cases for salary calculation"""
    
    def test_calculate_salary_india_deduction(self, client):
        """Test salary calculation with India 10% deduction"""
        response = client.post('/api/employees', json={
            'full_name': 'Test Employee',
            'job_title': 'Engineer',
            'country': 'India',
            'salary': 50000
        })
        employee_id = response.json()['id']
        
        response = client.get(f'/api/salary/calculate/{employee_id}?gross_salary=100000')
        
        assert response.status_code == 200
        data = response.json()
        assert data['country'] == 'India'
        assert data['deduction_rate'] == 10.0
        assert data['deductions'] == 10000.0
        assert data['net_salary'] == 90000.0
    
    def test_calculate_salary_us_deduction(self, client):
        """Test salary calculation with US 12% deduction"""
        response = client.post('/api/employees', json={
            'full_name': 'US Employee',
            'job_title': 'Manager',
            'country': 'United States',
            'salary': 80000
        })
        employee_id = response.json()['id']
        
        response = client.get(f'/api/salary/calculate/{employee_id}?gross_salary=100000')
        
        assert response.status_code == 200
        data = response.json()
        assert data['country'] == 'United States'
        assert data['deduction_rate'] == 12.0
        assert data['deductions'] == 12000.0
        assert data['net_salary'] == 88000.0
    
    def test_calculate_salary_no_deduction(self, client):
        """Test salary calculation with no deduction for other countries"""
        response = client.post('/api/employees', json={
            'full_name': 'Canada Employee',
            'job_title': 'Developer',
            'country': 'Canada',
            'salary': 70000
        })
        employee_id = response.json()['id']
        
        response = client.get(f'/api/salary/calculate/{employee_id}?gross_salary=100000')
        
        assert response.status_code == 200
        data = response.json()
        assert data['country'] == 'Canada'
        assert data['deduction_rate'] == 0.0
        assert data['deductions'] == 0.0
        assert data['net_salary'] == 100000.0
    
    def test_calculate_salary_employee_not_found(self, client):
        """Test salary calculation for non-existent employee"""
        response = client.get('/api/salary/calculate/9999?gross_salary=100000')
        
        assert response.status_code == 404
