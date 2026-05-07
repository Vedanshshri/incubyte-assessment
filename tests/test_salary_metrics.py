"""Test cases for salary metrics"""
import pytest

class TestSalaryMetrics:
    """Test cases for salary metrics endpoints"""
    
    def setup_method(self, method):
        """Setup sample employees for each test"""
        pass
    
    def test_country_metrics_india(self, client):
        """Test salary metrics for India"""
        # Create India employees
        employees_data = [
            {'full_name': 'Raj Kumar', 'job_title': 'Software Engineer', 'country': 'India', 'salary': 50000},
            {'full_name': 'Priya Singh', 'job_title': 'Software Engineer', 'country': 'India', 'salary': 60000},
            {'full_name': 'Amit Patel', 'job_title': 'DevOps Engineer', 'country': 'India', 'salary': 70000},
        ]
        for emp in employees_data:
            client.post('/api/employees', json=emp)
        
        response = client.get('/api/salary/metrics/country/India')
        
        assert response.status_code == 200
        data = response.json()
        assert data['country'] == 'India'
        assert data['count'] == 3
        assert data['minimum_salary'] == 50000
        assert data['maximum_salary'] == 70000
        assert data['average_salary'] == 60000.0
    
    def test_country_metrics_us(self, client):
        """Test salary metrics for United States"""
        # Create US employees
        employees_data = [
            {'full_name': 'John Smith', 'job_title': 'Product Manager', 'country': 'United States', 'salary': 90000},
            {'full_name': 'Sarah Johnson', 'job_title': 'Product Manager', 'country': 'United States', 'salary': 100000},
            {'full_name': 'Mike Brown', 'job_title': 'Software Engineer', 'country': 'United States', 'salary': 110000},
        ]
        for emp in employees_data:
            client.post('/api/employees', json=emp)
        
        response = client.get('/api/salary/metrics/country/United States')
        
        assert response.status_code == 200
        data = response.json()
        assert data['country'] == 'United States'
        assert data['count'] == 3
        assert data['minimum_salary'] == 90000
        assert data['maximum_salary'] == 110000
        assert data['average_salary'] == 100000.0
    
    def test_country_metrics_canada(self, client):
        """Test salary metrics for Canada"""
        # Create Canada employees
        employees_data = [
            {'full_name': 'Tom Anderson', 'job_title': 'Data Analyst', 'country': 'Canada', 'salary': 65000},
            {'full_name': 'Emily White', 'job_title': 'Software Engineer', 'country': 'Canada', 'salary': 75000},
        ]
        for emp in employees_data:
            client.post('/api/employees', json=emp)
        
        response = client.get('/api/salary/metrics/country/Canada')
        
        assert response.status_code == 200
        data = response.json()
        assert data['country'] == 'Canada'
        assert data['count'] == 2
        assert data['minimum_salary'] == 65000
        assert data['maximum_salary'] == 75000
        assert data['average_salary'] == 70000.0
    
    def test_country_metrics_not_found(self, client):
        """Test country metrics for non-existent country"""
        response = client.get('/api/salary/metrics/country/NonExistent')
        
        assert response.status_code == 404
    
    def test_job_title_metrics_software_engineer(self, client):
        """Test average salary for Software Engineer role"""
        # Create employees with various job titles
        employees_data = [
            {'full_name': 'Raj Kumar', 'job_title': 'Software Engineer', 'country': 'India', 'salary': 50000},
            {'full_name': 'Priya Singh', 'job_title': 'Software Engineer', 'country': 'India', 'salary': 60000},
            {'full_name': 'Mike Brown', 'job_title': 'Software Engineer', 'country': 'United States', 'salary': 110000},
            {'full_name': 'Emily White', 'job_title': 'Software Engineer', 'country': 'Canada', 'salary': 75000},
            {'full_name': 'John Smith', 'job_title': 'Product Manager', 'country': 'United States', 'salary': 90000},
        ]
        for emp in employees_data:
            client.post('/api/employees', json=emp)
        
        response = client.get('/api/salary/metrics/job-title/Software Engineer')
        
        assert response.status_code == 200
        data = response.json()
        assert data['job_title'] == 'Software Engineer'
        assert data['count'] == 4
        # Average of 50000, 60000, 110000, 75000 = 73750
        assert data['average_salary'] == 73750.0
    
    def test_job_title_metrics_product_manager(self, client):
        """Test average salary for Product Manager role"""
        # Create employees
        employees_data = [
            {'full_name': 'John Smith', 'job_title': 'Product Manager', 'country': 'United States', 'salary': 90000},
            {'full_name': 'Sarah Johnson', 'job_title': 'Product Manager', 'country': 'United States', 'salary': 100000},
            {'full_name': 'Raj Kumar', 'job_title': 'Software Engineer', 'country': 'India', 'salary': 50000},
        ]
        for emp in employees_data:
            client.post('/api/employees', json=emp)
        
        response = client.get('/api/salary/metrics/job-title/Product Manager')
        
        assert response.status_code == 200
        data = response.json()
        assert data['job_title'] == 'Product Manager'
        assert data['count'] == 2
        # Average of 90000 and 100000 = 95000
        assert data['average_salary'] == 95000.0
    
    def test_job_title_metrics_data_analyst(self, client):
        """Test average salary for Data Analyst role"""
        # Create employee
        client.post('/api/employees', json={
            'full_name': 'Tom Anderson',
            'job_title': 'Data Analyst',
            'country': 'Canada',
            'salary': 65000
        })
        
        response = client.get('/api/salary/metrics/job-title/Data Analyst')
        
        assert response.status_code == 200
        data = response.json()
        assert data['job_title'] == 'Data Analyst'
        assert data['count'] == 1
        assert data['average_salary'] == 65000.0
    
    def test_job_title_metrics_not_found(self, client):
        """Test job title metrics for non-existent role"""
        response = client.get('/api/salary/metrics/job-title/NonExistentRole')
        
        assert response.status_code == 404
    
    def test_country_single_employee(self, client):
        """Test country metrics with single employee"""
        # Create single employee
        client.post('/api/employees', json={
            'full_name': 'David Green',
            'job_title': 'Software Engineer',
            'country': 'United Kingdom',
            'salary': 55000
        })
        
        response = client.get('/api/salary/metrics/country/United Kingdom')
        
        assert response.status_code == 200
        data = response.json()
        assert data['count'] == 1
        assert data['minimum_salary'] == 55000
        assert data['maximum_salary'] == 55000
        assert data['average_salary'] == 55000.0
