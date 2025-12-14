import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture
def clean_account():
  pesel = "90010100000"
  requests.delete(f"{BASE_URL}/api/accounts/{pesel}")
  return pesel

def test_create_account(clean_account):
  pesel = clean_account
  payload = {
    "name": "Test",
    "surname": "User",
    "pesel": pesel
  }
  
  response = requests.post(f"{BASE_URL}/api/accounts", json=payload)
  
  assert response.status_code == 201
  assert response.json()["message"] == "Account created"

def test_get_account_by_pesel(clean_account):
  pesel = clean_account
  requests.post(f"{BASE_URL}/api/accounts", json={"name": "Jan", "surname": "Kowalski", "pesel": pesel})
  
  response = requests.get(f"{BASE_URL}/api/accounts/{pesel}")
  
  assert response.status_code == 200
  data = response.json()
  assert data["name"] == "Jan"
  assert data["pesel"] == pesel
  assert data["balance"] == 0

def test_get_account_count(clean_account):
  initial_response = requests.get(f"{BASE_URL}/api/accounts/count")
  initial_count = initial_response.json()["count"]
  
  requests.post(f"{BASE_URL}/api/accounts", json={"name": "Count", "surname": "Test", "pesel": clean_account})
  
  new_response = requests.get(f"{BASE_URL}/api/accounts/count")
  new_count = new_response.json()["count"]
  
  assert new_count == initial_count + 1

def test_get_account_by_pesel_404():
  response = requests.get(f"{BASE_URL}/api/accounts/00000000000")
  assert response.status_code == 404

def test_update_account(clean_account):
  pesel = clean_account
  requests.post(f"{BASE_URL}/api/accounts", json={"name": "OldName", "surname": "OldSurname", "pesel": pesel})
  
  update_data = {"surname": "NewSurname"}
  response = requests.patch(f"{BASE_URL}/api/accounts/{pesel}", json=update_data)
  
  assert response.status_code == 200
  
  check = requests.get(f"{BASE_URL}/api/accounts/{pesel}")
  data = check.json()
  assert data["surname"] == "NewSurname"
  assert data["name"] == "OldName"

def test_delete_account(clean_account):
  pesel = clean_account
  requests.post(f"{BASE_URL}/api/accounts", json={"name": "To", "surname": "Delete", "pesel": pesel})
  
  response = requests.delete(f"{BASE_URL}/api/accounts/{pesel}")
  assert response.status_code == 200
  
  check = requests.get(f"{BASE_URL}/api/accounts/{pesel}")
  assert check.status_code == 404