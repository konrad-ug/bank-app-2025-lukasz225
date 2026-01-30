import requests
import pytest

BASE_URL = "http://127.0.0.1:5000"

def test_save_and_load_flow():
  pesel = "55050512345"
  requests.post(f"{BASE_URL}/api/accounts", json={
    "name": "Test", "surname": "Persist", "pesel": pesel
  })
  
  resp_save = requests.post(f"{BASE_URL}/api/accounts/save")
  assert resp_save.status_code == 200

  requests.delete(f"{BASE_URL}/api/accounts/{pesel}")
  check = requests.get(f"{BASE_URL}/api/accounts/{pesel}")
  assert check.status_code == 404

  resp_load = requests.post(f"{BASE_URL}/api/accounts/load")
  assert resp_load.status_code == 200

  check_again = requests.get(f"{BASE_URL}/api/accounts/{pesel}")
  assert check_again.status_code == 200
  assert check_again.json()['name'] == "Test"