def test_create_organisation(client):
    payload = {
        "org_name": "Test Org",
        "org_type": "IT",
        "branch_name": "Main",
        "address": "123 Test Street",
        "contact_number": "1234567890",
        "email": "org@example.com"
    }
    response = client.post("/organisations/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["org_name"] == payload["org_name"]

def test_create_department(client):
    payload = {
        "dept_name": "HR"
    }
    response = client.post("/departments/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["dept_name"] == payload["dept_name"]

def test_create_designation(client):
    payload = {
        "designation_name": "Manager"
    }
    response = client.post("/designations/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["designation_name"] == payload["designation_name"]

def test_create_employee(client):
    # Create department
    dept_resp = client.post("/departments/", json={"dept_name": "IT"})
    dept_id = dept_resp.json()["dept_id"]

    # Create designation
    desig_resp = client.post("/designations/", json={"designation_name": "Developer"})
    desig_id = desig_resp.json()["designation_id"]

    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "9876543210",
        "department_id": dept_id,
        "designation_id": desig_id
    }
    response = client.post("/employees/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == payload["first_name"]
    assert data["department_id"] == dept_id
    assert data["designation_id"] == desig_id

def test_create_payroll(client):
    # Create employee first
    emp_resp = client.post("/employees/", json={
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com"
        # Include department_id, designation_id if required
    })
    emp_id = emp_resp.json()["employee_id"]

    payload = {
        "employee_id": emp_id,
        "pay_period": "2025-10",
        "gross_salary": 60000.00,
        "total_deductions": 15000.00,
        "net_salary": 45000.00
    }
    response = client.post("/payroll/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["employee_id"] == emp_id
    assert float(data["gross_salary"]) == 60000
