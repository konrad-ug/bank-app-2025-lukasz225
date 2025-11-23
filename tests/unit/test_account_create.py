import pytest
from src.account import PersonalAccount, BusinessAccount

class TestPersonalAccountCreation:
  
  def test_account_creation_valid(self):
    account = PersonalAccount("John", "Doe", "02340174842")
    assert account.first_name == "John"
    assert account.last_name == "Doe"
    assert account.balance == 0
    assert account.pesel == '02340174842'

  @pytest.mark.parametrize("invalid_pesel", [
    "123",
    "1234567890123",
    None,
    True,
    12345678901
  ])
  def test_pesel_invalid(self, invalid_pesel):
    account = PersonalAccount("Jane", "Doe", invalid_pesel)
    assert account.pesel == "Invalid"

  @pytest.mark.parametrize("pesel, promo_code, expected_balance", [
    ("02320174842", "PROM_XYZ", 50),
    ("59010112345", "PROM_ABC", 0),
    ("123", "PROM_ABC", 0),
    ("02340174842", "XYZ", 0),
    ("02340174842", None, 0),
  ])
  def test_promo_code_application(self, pesel, promo_code, expected_balance):
    account = PersonalAccount("Jane", "Doe", pesel, promo_code=promo_code)
    assert account.balance == expected_balance


class TestBusinessAccountCreation:
  
  def test_creation_valid_nip(self):
    account = BusinessAccount("Firma XYZ S.A.", "1234567890")
    assert account.company_name == "Firma XYZ S.A."
    assert account.nip == "1234567890"

  @pytest.mark.parametrize("invalid_nip", [
    "123",
    "1234567890123",
    1234567890
  ])
  def test_nip_invalid(self, invalid_nip):
    account = BusinessAccount("Firma Krzak", invalid_nip)
    assert account.nip == "Invalid"


class TestPersonalAccountTransfers:
  def test_receive_transfer_increases_balance(self):
    account = PersonalAccount("Test", "user", "00210112345")
    account.receive_transfer(100)
    assert account.balance == 100
  
  def test_send_transfer_success(self):
    account = PersonalAccount("Test", "User", "00210112345")
    account.balance = 500
    assert account.send_transfer(200) is True
    assert account.balance == 300

  def test_send_express_transfer_personal(self):
    account = PersonalAccount("Test", "User", "00210112345")
    account.balance = 200
    assert account.send_express_transfer(100) is True
    assert account.balance == 99


class TestAccountHistory:
  def test_history_flow(self):
    account = PersonalAccount("Test", "User", "00210112345")
    account.receive_transfer(500)
    account.send_express_transfer(300)
    assert account.history == [500, -300, -1]


class TestBusinessAccountTransfers:
  def test_business_receive_transfer(self):
    account = BusinessAccount("Test Biz", "1112223344")
    account.receive_transfer(1000)
    assert account.balance == 1000
    
  def test_business_send_transfer_success(self):
    account = BusinessAccount("Test Biz", "1112223344")
    account.balance = 2000
    success = account.send_transfer(500)
    assert account.balance == 1500
    assert success == True

  def test_business_send_transfer_fail_insufficient_funds(self):
    account = BusinessAccount("Test Biz", "1112223344")
    account.balance = 100
    failure = account.send_transfer(500)
    assert account.balance == 100
    assert failure == False

  def test_business_express_transfer_success_with_fee(self):
    account = BusinessAccount("Test Biz", "1112223344")
    account.balance = 1000
    success = account.send_express_transfer(500)
    assert account.balance == 495
    assert success == True

  def test_business_express_transfer_allowed_to_go_negative(self):
    account = BusinessAccount("Test Biz", "1112223344")
    account.balance = 500
    success = account.send_express_transfer(500)
    assert account.balance == -5
    assert success == True

  def test_business_express_transfer_fail_insufficient_for_amount(self):
    account = BusinessAccount("Test Biz", "1112223344")
    account.balance = 499
    failure = account.send_express_transfer(500)
    assert account.balance == 499
    assert failure == False