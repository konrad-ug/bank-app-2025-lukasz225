import pytest
from src.account import PersonalAccount, BusinessAccount

VALID_PESEL_NO_PROMO = "50010112345"

@pytest.fixture
def personal_account():
  return PersonalAccount("John", "Johnson", VALID_PESEL_NO_PROMO)

@pytest.fixture
def business_account():
  return BusinessAccount("ABC Company", "1234567890")