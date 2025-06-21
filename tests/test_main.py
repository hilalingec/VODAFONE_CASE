from fastapi.testclient import TestClient
from app.main import app
import random 
from faker import Faker

import warnings
warnings.filterwarnings('ignore') 


client = TestClient(app)
faker = Faker()

def test_insert_and_get_user_with_date():
    user_id = random.randint(0,1000)
    name = faker.first_name()
    surname = faker.last_name()

    response = client.post("/insert", json={
        "id": user_id,
        "name": name,
        "surname": surname
    })
    assert response.status_code == 200
    assert response.json()["status"] == "saved"

    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200
    result = response.json()
    assert "source" in result
    assert "data" in result
    assert "date" in result["data"]
