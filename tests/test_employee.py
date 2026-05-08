"""Test cases for Employee CRUD operations"""
import pytest

class TestEmployeeCRUD:
    """Test cases for Employee CRUD operations"""
    
    def test_create_employee(self, client):
        """Test creating a new employee"""
        response = client.post('/api/employees', json={
            'full_name': 'Jane Smith',
            'job_title': 'Product Manager',
            'country': 'United States',
            'salary': 75000
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data['full_name'] == 'Jane Smith'
        assert data['job_title'] == 'Product Manager'
        assert data['country'] == 'United States'
        assert data['salary'] == 75000
    
    def test_create_employee_missing_fields(self, client):
        """Test creating employee with missing required fields"""
        response = client.post('/api/employees', json={
            'full_name': 'Jane Smith',
            'job_title': 'Product Manager'
        })
        
        assert response.status_code == 422
    
    def test_get_all_employees(self, client):
        """Test retrieving all employees"""
        # First create an employee
        client.post('/api/employees', json={
            'full_name': 'John Doe',
            'job_title': 'Software Engineer',
            'country': 'India',
            'salary': 50000
        })
        
        response = client.get('/api/employees')
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['full_name'] == 'John Doe'
    
    def test_get_employee_by_id(self, client):
        """Test retrieving a specific employee"""
        # Create an employee
        create_response = client.post('/api/employees', json={
            'full_name': 'John Doe',
            'job_title': 'Software Engineer',
            'country': 'India',
            'salary': 50000
        })
        employee_id = create_response.json()['id']
        
        response = client.get(f'/api/employees/{employee_id}')
        
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == employee_id
        assert data['full_name'] == 'John Doe'
    
    def test_get_employee_not_found(self, client):
        """Test retrieving non-existent employee"""
        response = client.get('/api/employees/9999')
        
        assert response.status_code == 404
    
    def test_update_employee(self, client):
        """Test updating an employee"""
        # Create an employee
        create_response = client.post('/api/employees', json={
            'full_name': 'John Doe',
            'job_title': 'Software Engineer',
            'country': 'India',
            'salary': 50000
        })
        employee_id = create_response.json()['id']
        
        response = client.put(f'/api/employees/{employee_id}', json={
            'job_title': 'Senior Software Engineer',
            'salary': 80000
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data['job_title'] == 'Senior Software Engineer'
        assert data['salary'] == 80000
        assert data['full_name'] == 'John Doe'
    
    def test_update_employee_not_found(self, client):
        """Test updating non-existent employee"""
        response = client.put('/api/employees/9999', json={
            'salary': 60000
        })
        
        assert response.status_code == 404
    
    def test_delete_employee(self, client):
        """Test deleting an employee"""
        # Create an employee
        create_response = client.post('/api/employees', json={
            'full_name': 'John Doe',
            'job_title': 'Software Engineer',
            'country': 'India',
            'salary': 50000
        })
        employee_id = create_response.json()['id']
        
        response = client.delete(f'/api/employees/{employee_id}')
        
        assert response.status_code == 200
        
        # Verify employee is deleted
        response = client.get(f'/api/employees/{employee_id}')
        assert response.status_code == 404
    
    def test_delete_employee_not_found(self, client):
        """Test deleting non-existent employee"""
        response = client.delete('/api/employees/9999')
        
        assert response.status_code == 404
    
    def test_create_employee_with_float_salary(self, client):
        """Test creating employee with float salary"""
        response = client.post('/api/employees', json={
            'full_name': 'Bob Johnson',
            'job_title': 'Developer',
            'country': 'India',
            'salary': 45000.50
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data['salary'] == 45000.50
    
    def test_create_employee_with_negative_salary(self, client):
        """Test that creating employee with negative salary is rejected"""
        response = client.post('/api/employees', json={
            'full_name': 'Invalid Employee',
            'job_title': 'Developer',
            'country': 'India',
            'salary': -50000
        })
        
        assert response.status_code == 422
        
    def test_create_employee_with_zero_salary(self, client):
        """Test that creating employee with zero salary is rejected"""
        response = client.post('/api/employees', json={
            'full_name': 'Invalid Employee',
            'job_title': 'Developer',
            'country': 'India',
            'salary': 0
        })
        
        assert response.status_code == 422
    
    def test_update_employee_with_negative_salary(self, client):
        """Test that updating employee with negative salary is rejected"""
        # Create an employee
        create_response = client.post('/api/employees', json={
            'full_name': 'John Doe',
            'job_title': 'Software Engineer',
            'country': 'India',
            'salary': 50000
        })
        employee_id = create_response.json()['id']
        
        response = client.put(f'/api/employees/{employee_id}', json={
            'salary': -80000
        })
        
        assert response.status_code == 422

    # --- Edge case tests ---

    def test_get_all_employees_empty_database(self, client):
        """Test getting employees when database is empty returns empty list"""
        response = client.get('/api/employees')
        assert response.status_code == 200
        assert response.json() == []

    def test_create_employee_empty_name(self, client):
        """Test that empty full_name is rejected"""
        response = client.post('/api/employees', json={
            'full_name': '',
            'job_title': 'Developer',
            'country': 'India',
            'salary': 50000
        })
        assert response.status_code == 422

    def test_create_employee_whitespace_name(self, client):
        """Test that whitespace-only full_name is rejected"""
        response = client.post('/api/employees', json={
            'full_name': '   ',
            'job_title': 'Developer',
            'country': 'India',
            'salary': 50000
        })
        assert response.status_code == 422

    def test_create_employee_empty_job_title(self, client):
        """Test that empty job_title is rejected"""
        response = client.post('/api/employees', json={
            'full_name': 'John Doe',
            'job_title': '',
            'country': 'India',
            'salary': 50000
        })
        assert response.status_code == 422

    def test_create_employee_empty_country(self, client):
        """Test that empty country is rejected"""
        response = client.post('/api/employees', json={
            'full_name': 'John Doe',
            'job_title': 'Developer',
            'country': '',
            'salary': 50000
        })
        assert response.status_code == 422

    def test_update_employee_empty_name(self, client):
        """Test that updating full_name to empty string is rejected"""
        create_response = client.post('/api/employees', json={
            'full_name': 'John Doe',
            'job_title': 'Software Engineer',
            'country': 'India',
            'salary': 50000
        })
        employee_id = create_response.json()['id']

        response = client.put(f'/api/employees/{employee_id}', json={
            'full_name': ''
        })
        assert response.status_code == 422

    def test_update_employee_whitespace_name(self, client):
        """Test that updating full_name to whitespace-only string is rejected"""
        create_response = client.post('/api/employees', json={
            'full_name': 'John Doe',
            'job_title': 'Software Engineer',
            'country': 'India',
            'salary': 50000
        })
        employee_id = create_response.json()['id']

        response = client.put(f'/api/employees/{employee_id}', json={
            'full_name': '   '
        })
        assert response.status_code == 422

    def test_update_employee_no_fields_is_noop(self, client):
        """Test that updating with empty body leaves employee unchanged"""
        create_response = client.post('/api/employees', json={
            'full_name': 'John Doe',
            'job_title': 'Software Engineer',
            'country': 'India',
            'salary': 50000
        })
        employee_id = create_response.json()['id']

        response = client.put(f'/api/employees/{employee_id}', json={})
        assert response.status_code == 200
        data = response.json()
        assert data['full_name'] == 'John Doe'
        assert data['salary'] == 50000

    def test_get_employee_invalid_id_type(self, client):
        """Test that a non-integer employee ID returns 422"""
        response = client.get('/api/employees/abc')
        assert response.status_code == 422

    def test_employee_response_has_timestamps(self, client):
        """Test that created employee response includes timestamps"""
        response = client.post('/api/employees', json={
            'full_name': 'John Doe',
            'job_title': 'Software Engineer',
            'country': 'India',
            'salary': 50000
        })
        assert response.status_code == 201
        data = response.json()
        assert 'created_at' in data
        assert data['created_at'] is not None
