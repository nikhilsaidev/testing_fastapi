import pytest
from fastapi.testclient import TestClient
from main import app

# Create a TestClient for FastAPI
#### THIS CREATS A TEST CLIENT WITHOUT STATARTING THE ACTUAL HTTP SERVER
client = TestClient(app)


##### WHAT ARE FIXTURES
#####Fixtures are like preparing the test environment before running tests. Think of it as setting up everything needed before a test starts and cleaning up after it ends.

@pytest.fixture
def test_client():
    """Fixture to create a fresh test client."""
    return client

# Example :
# Imagine you are testing a new mobile phone.
# Before testing, you charge the battery, insert a SIM card, and turn on the phone.
# After testing, you turn it off and remove the SIM if needed.


### WHY FIXTURES?????HERE IT IS
# @pytest.fixture
# def test_client():
#     return TestClient(app)

# # This test automatically uses the test_client fixture
# def test_example(test_client):
#     response = test_client.get("/users/1")
#     assert response.status_code == 200

# Without a fixture, you would have to create TestClient(app) in every test! Using fixtures makes the code cleaner and reusable.WE USE MOSTLY THIS FOR SETTING UP DATABASE AND STUFF LIKE THAT. AND ANOTHER EXAMPLE IS CREATING A SAMPLE DATA LIKE A DATABASE FOR ALL THE INPUTS.


def test_get_existing_user(test_client):
    """Test fetching an existing user."""
    response = test_client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"

def test_get_non_existing_user(test_client):
    """Test fetching a user that does not exist."""
    response = test_client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_create_user_success(test_client):
    """Test creating a new user successfully."""
    new_user = {"name": "Charlie", "email": "charlie@example.com"}
    response = test_client.post("/users", json=new_user)
    
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["name"] == "Charlie"

def test_create_user_invalid_data(test_client):
    """Test creating a user with missing fields."""
    response = test_client.post("/users", json={})
    
    assert response.status_code == 422  # FastAPI automatically handles validation errors


####  THE ABOVE WAY IS TO TEST FOR SINGLE INPUTS FOR ANY API'S, BUT INSTEAD OF THIS WE CAN WRITE A PARAMETERIZED TESTING WHICH CAN BE SOLVED LIKE THIS. IT IS LIKE GIVING MULTIPLE INPUTS AT A TIME.
####  YOU CAN USE ANY ONE OF THEM


@pytest.mark.parametrize(
    "user_id, expected_status, expected_name",
    [
        (1, 200, "Alice"),  # Existing user
        (999, 404, None)  # Non-existing user
    ]
)
def test_get_user(test_client, user_id, expected_status, expected_name):
    """Test fetching users (both existing and non-existing)."""
    response = test_client.get(f"/users/{user_id}")
    
    assert response.status_code == expected_status
    
    if expected_status == 200:
        assert response.json()["name"] == expected_name
    else:
        assert response.json()["detail"] == "User not found"

@pytest.mark.parametrize(
    "user_data, expected_status, expected_response_keys",
    [
        ({"name": "Charlie", "email": "charlie@example.com"}, 201, ["id", "name"]),
        ({}, 422, [])  # Invalid request with missing fields
    ]
)
def test_create_user(test_client, user_data, expected_status, expected_response_keys):
    """Test creating users with valid and invalid data."""
    response = test_client.post("/users", json=user_data)
    
    assert response.status_code == expected_status
    
    if expected_status == 201:
        for key in expected_response_keys:
            assert key in response.json()
        assert response.json()["name"] == user_data["name"]
        
        
        
        
##### MOCKING replaces real objects with fake ones during testing. MAINLY IT IS USED FOR 

# Avoiding API calls in tests.
# Simulating external services (e.g., databases, file systems).
# Preventing side effects like sending emails.

