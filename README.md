# Salary Management API

A RESTful API built with **FastAPI** and **SQLite** for managing employees, calculating salary deductions, and querying salary metrics.

---

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy (ORM)
- Pydantic v2 (validation)
- SQLite (via `aiosqlite`-free sync driver)
- pytest + httpx (testing)

---

## Getting Started

### Prerequisites

```bash
pip install -r requirements.txt
```

### Run the server

```bash
python main.py
```

API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

### Run tests

```bash
pytest tests/ -v
```

---

## API Endpoints

### Employees

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/employees` | Create a new employee |
| `GET` | `/api/employees` | List all employees |
| `GET` | `/api/employees/{id}` | Get employee by ID |
| `PUT` | `/api/employees/{id}` | Update employee fields |
| `DELETE` | `/api/employees/{id}` | Delete an employee |

**Employee fields:**

| Field | Type | Validation |
|-------|------|------------|
| `full_name` | string | required |
| `job_title` | string | required |
| `country` | string | required |
| `salary` | float | required, must be > 0 |

### Salary Calculation

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/salary/calculate/{employee_id}` | Calculate deductions and net salary |

**Deduction rules:**

| Country | TDS Rate |
|---------|----------|
| India | 10% |
| United States | 12% |
| All others | 0% |

### Salary Metrics

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/salary/metrics/country/{country}` | Min, max, avg salary for a country |
| `GET` | `/api/salary/metrics/job-title/{job_title}` | Average salary for a job title |

---

## Project Structure

```
.
├── main.py                  # FastAPI app entry point, router registration
├── app/
│   ├── database.py          # SQLAlchemy engine and session setup
│   ├── models.py            # Employee ORM model
│   ├── schemas.py           # Pydantic request/response schemas
│   └── routes/
│       ├── employee.py      # Employee CRUD endpoints
│       └── salary.py        # Salary calculation and metrics endpoints
├── tests/
│   ├── conftest.py          # In-memory SQLite test DB, per-test reset fixture
│   ├── test_employee.py     # Employee CRUD tests (13 cases)
│   ├── test_salary_calculation.py  # Salary deduction tests (6 cases)
│   └── test_salary_metrics.py      # Metrics endpoint tests (9 cases)
├── requirements.txt
└── pytest.ini
```

---

## Design Decisions

- **Per-test DB reset**: `conftest.py` uses an `autouse=True` fixture that drops and recreates all tables before and after every test. This guarantees full isolation — no state bleeds between tests.
- **Salary validation at schema level**: `EmployeeCreate` and `EmployeeUpdate` use `Field(gt=0)` so negative or zero salaries are rejected with a `422` before they ever reach the database.
- **Deduction logic is pure**: `calculate_salary_deductions()` in `salary.py` is a plain function separate from the route handler, making it easy to test in isolation or reuse.
- **In-memory SQLite for tests**: Uses `StaticPool` to keep the same connection alive across the test session while still being isolated per test via table teardown.

---

## TDD Approach

Development followed a strict red → green → refactor cycle, with each commit representing a meaningful step:

1. `test(red)` — Write failing tests for the feature
2. `feat(green)` — Write minimal implementation to make tests pass
3. `refactor` — Clean up without breaking tests

Commit history reflects this progression for each of the three feature areas: employee CRUD, salary calculation, and salary metrics.

---

## Implementation Details

### Where AI Was Used

AI (GitHub Copilot) was used in the following specific, limited ways:

- **Commit messages**: Suggested conventional commit format (`feat:`, `test:`, `refactor:`) to ensure messages were descriptive and consistent. All messages were reviewed and edited manually.
- **README**: This file was drafted with AI assistance using a prompt like: *"Write a README for a FastAPI salary management API covering setup, endpoints, deduction rules, project structure, and design decisions."* Content was reviewed and trimmed to what is accurate.
- **Initial project setup**: Boilerplate such as `pytest.ini`, `requirements.txt`, and the `conftest.py` in-memory DB wiring were scaffolded with AI and then adjusted (e.g., adding `StaticPool`, the `autouse` reset fixture).
- **Error handling patterns**: AI suggested using `HTTPException` with appropriate status codes (404 for not found, 422 for validation errors already handled by Pydantic). The actual placement and conditions were written manually.

### What Was Written Manually

- All business logic: deduction rate lookup, metrics aggregation (`min`, `max`, `avg`)
- All test assertions and test data — the test cases reflect deliberate choices about edge cases (negative salary, float salary, single-employee country, cross-country job title averages)
- Schema constraints (`gt=0` for salary validation)
- The decision to isolate deduction logic into a pure helper function

AI was not used to generate test cases wholesale, write route implementations from scratch, or make architectural decisions.
