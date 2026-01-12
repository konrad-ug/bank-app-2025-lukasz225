import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:5000"

class TestPerformance:

  def test_create_and_delete_account_performance(self):
    pesel = "90010100000"
    for i in range(100):
      payload = {"name": "Perf", "surname": "Test", "pesel": pesel}
      response_post = requests.post(f"{BASE_URL}/api/accounts", json=payload, timeout=0.5)
      assert response_post.status_code == 201
      
      response_del = requests.delete(f"{BASE_URL}/api/accounts/{pesel}", timeout=0.5)
      assert response_del.status_code == 200

  def test_multiple_transfers_performance(self):
    pesel = "80010199999"
    requests.delete(f"{BASE_URL}/api/accounts/{pesel}")
    requests.post(f"{BASE_URL}/api/accounts", json={"name": "P", "surname": "T", "pesel": pesel})
    
    amount = 10
    total_transfers = 100
    
    for i in range(total_transfers):
      payload = {"amount": amount, "type": "incoming"}
      response = requests.post(f"{BASE_URL}/api/accounts/{pesel}/transfer", json=payload, timeout=0.5)
      assert response.status_code == 200
    
    check = requests.get(f"{BASE_URL}/api/accounts/{pesel}")
    assert check.json()["balance"] == amount * total_transfers

  def test_mass_create_then_delete(self):
    pesels = [str(10000000000 + i) for i in range(1000)]
    
    for p in pesels:
      res = requests.post(f"{BASE_URL}/api/accounts", 
                          json={"name": "N", "surname": "S", "pesel": p}, timeout=0.5)
      assert res.status_code == 201
    
    for p in pesels:
      res = requests.delete(f"{BASE_URL}/api/accounts/{p}", timeout=0.5)
      assert res.status_code == 200