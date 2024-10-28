from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/register",
        json={"username": "testuser", "password": "testpassword", "email": "test@example.com"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}
