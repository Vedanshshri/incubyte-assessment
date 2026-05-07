"""Test cases for salary calculation"""
import pytest

class TestSalaryCalculation:
    """Test cases for salary calculation"""
    
    def test_calculate_salary_india_deduction(self, client):
        """Test salary calculation with India 10% deduction"""
        # Create India employee
        response = client.post('/api/employees', json={
            'full_name': 'Test Employee',
            'job_title': 'Engineer',
            'country': 'India',
            'salary': 50000
        })
        employee_id = response.json()['id']
        
        response = client.post(f'/api/salary/calculate/{employee_id}', json={
            'gross_salary': 100000
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data['country'] == 'India'
        assert data['deduction_rate'] == 10.0
        assert data['deductions'] == 10000.0
        assert data['net_salary'] == 90000.0
    
    def test_calculate_salary_us_deduction(self, client):
        """Test salary calculation with US 12% deduction"""
        # Create US employee
        response = client.post('/api/employees', json={
            'full_name': 'US Employee',
            'job_title': 'Manager',
            'country': 'United States',
            'salary': 80000
        })
        employee_id = response.json()['id']
        
        response = client.post(f'/api/salary/calculate/{employee_id}', json={
            'gross_salary': 100000
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data['country'] == 'United States'
        assert data['deduction_rate'] == 12.0
        assert data['deductions'] == 12000.0
        assert data['net_salary'] == 88000.0
    
    def test_calculate_salary_no_deduction(self, client):
        """Test salary calculation with no deduction for other countries"""
        # Create Canada employee (not in deduction list)
        response = client.post('/api/employees', json={
            'full_name': 'Canada Employee',
            'job_title': 'Developer',
            'country': 'Canada',
            'salary': 70000
        })
        employee_id = response.json()['id']
        
        response = client.post(f'/api/salary/calculate/{employee_id}', json={
            'gross_salary': 100000
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data['country'] == 'Canada'
        assert data['deduction_rate'] == 0.0
        assert data['deductions'] == 0.0
        assert data['net_salary'] == 100000.0
    
    def test_calculate_salary_employee_not_found(self, client):
        """Test salary calculation for non-existent employee"""
        response = client.post('/api/salary/calculate/9999', json={
            'gross_salary': 100000
        })
        
        assert response.status_code == 404
    
    def test_calculate_salary_missing_gross_salary(self, client):
        """Test salary calculation without gross_salary"""
        response = client.post('/api/employees', json={
            'full_name': 'Test',
            'job_title': 'Engineer',
            'country': 'India',
            'salary': 50000
        })
        employee_id = response.json()['id']
        
        response = client.post(f'/api/salary/calculate/{employee_id}', json={})
        
        assert response.status_code == 422
    
    def test_calculate_salary_various_amounts(self, client):
        """Test salary calculation with various amounts"""
        response = client.post('/api/employees', json={
            'full_name': 'Test',
            'job_title': 'Engineer',
            'country': 'India',
            'salary': 50000
        })
        employee_id = response.json()['id']
        
        test_cases = [50000, 123456.78, 1]
        
        for gross in test_cases:
            response = client.post(f'/api/salary/calculate/{employee_id}', json={
                'gross_salary': gross
            })
            assert response.status_code == 200
            data = response.json()
            assert data['gross_salary'] == gross
            assert data['deductions'] == round(gross * 0.10, 2)
            assert data['net_salary'] == round(gross * 0.90, 2)

    # --- Edge case tests ---

    def test_calculate_salary_negative_gross(self, client):
        """Test that negative gross salary is rejected"""
        response = client.post('/api/employees', json={
            'full_name': 'Test',
            'job_title': 'Engineer',
            'country': 'India',
            'salary': 50000
        })
        employee_id = response.json()['id']

        response = client.post(f'/api/salary/calculate/{employee_id}', json={
            'gross_salary': -10000
        })
        assert response.status_code == 422

    def test_calculate_salary_zero_gross(self, client):
        """Test that zero gross salary is rejected"""
        response = client.post('/api/employees', json={
            'full_name': 'Test',
            'job_title': 'Engineer',
            'country': 'India',
            'salary': 50000
        })
        employee_id = response.json()['id']

        response = client.post(f'/api/salary/calculate/{employee_id}', json={
            'gross_salary': 0
        })
        assert response.status_code == 422

    def test_calculate_salary_invalid_id_type(self, client):
        """Test that a non-integer employee ID returns 422"""
        response = client.post('/api/salary/calculate/abc', json={
            'gross_salary': 50000
        })
        assert response.status_code == 422

    def test_calculate_salary_float_precision(self, client):
        """Test deduction rounding with a fractional gross salary"""
        response = client.post('/api/employees', json={
            'full_name': 'Test',
            'job_title': 'Engineer',
            'country': 'India',
            'salary': 50000
        })
        employee_id = response.json()['id']

        gross = 99999.99
        response = client.post(f'/api/salary/calculate/{employee_id}', json={
            'gross_salary': gross
        })
        assert response.status_code == 200
        data = response.json()
        deductions = round(gross * 0.10, 2)
        net = round(gross - gross * 0.10, 2)
        assert data['deductions'] == deductions
        assert data['net_salary'] == net
        # Net + deductions must equal gross exactly
        assert round(data['net_salary'] + data['deductions'], 2) == gross

    def test_calculate_salary_response_structure(self, client):
        """Test that salary calculation response contains all expected fields"""
        response = client.post('/api/employees', json={
            'full_name': 'Test',
            'job_title': 'Engineer',
            'country': 'India',
            'salary': 50000
        })
        employee_id = response.json()['id']

        response = client.post(f'/api/salary/calculate/{employee_id}', json={
            'gross_salary': 100000
        })
        assert response.status_code == 200
        data = response.json()
        assert set(data.keys()) == {'employee_id', 'gross_salary', 'country', 'deduction_rate', 'deductions', 'net_salary'}
        assert data['employee_id'] == employee_id
