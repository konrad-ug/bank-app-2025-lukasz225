from src.account import PersonalAccount, BusinessAccount


class TestPersonalAccount:
  def test_account_creation(self):
    account = PersonalAccount("John", "Doe", "02340174842")
    assert account.first_name == "John"
    assert account.last_name == "Doe"
    assert account.balance == 0
    assert account.pesel == '02340174842'

  def test_pesel_too_short(self):
    account = PersonalAccount("Jane", "Doe", '123')
    assert account.pesel == "Invalid"

  def test_pesel_too_long(self):
    account = PersonalAccount("Jane", "Doe", '123123123123')
    assert account.pesel == "Invalid"

  def test_pesel_is_none(self):
    account = PersonalAccount("Jane", "Doe", None)
    assert account.pesel == "Invalid"

  def test_pesel_is_boolean(self):
    account = PersonalAccount("Jane", "Doe", True)
    assert account.pesel == "Invalid"

  def test_account_with_valid_promo_code_and_pesel(self):
    account = PersonalAccount("Jane", "Doe", "02320174842", promo_code="PROM_XYZ")
    assert account.balance == 50

  def test_promo_given_if_born_after_1960(self):
    account = PersonalAccount("Jane", "Doe", "02320174842", promo_code="PROM_ABC")
    assert account.balance == 50

  def test_no_promo_if_born_before_1960(self):
    account = PersonalAccount("Jane", "Doe", "59010112345", promo_code="PROM_ABC")
    assert account.balance == 0

  def test_no_promo_if_pesel_invalid(self):
    account = PersonalAccount("Jane", "Doe", "123", promo_code="PROM_ABC")
    assert account.balance == 0

  def test_no_promo_if_code_invalid(self):
    account = PersonalAccount("Jane", "Doe", "02340174842", promo_code="XYZ")
    assert account.balance == 0


class TestPersonalAccountTransfers:
  def test_receive_transfer_increases_balance(self):
    account = PersonalAccount("Test", "user", "00210112345")
    assert account.balance == 0
    account.receive_transfer(100)
    assert account.balance == 100
    account.receive_transfer(50)
    assert account.balance == 150

  def test_send_transfer_decreases_balance_on_success(self):
    account = PersonalAccount("Test", "User", "00210112345")
    account.balance = 500
    success = account.send_transfer(200)
    assert account.balance == 300
    assert success == True

  def test_send_transfer_fails_on_insufficient_funds(self):
    account = PersonalAccount("Test", "User", "00210112345")
    account.balance = 100
    failure = account.send_transfer(200)
    assert account.balance == 100
    assert failure == False

  def test_send_negative_transfer_fails(self):
    account = PersonalAccount("Test", "User", "00210112345")
    account.balance = 100
    failure = account.send_transfer(-50)
    assert account.balance == 100
    assert failure == False

  def test_personal_express_transfer_success_with_fee(self):
    account = PersonalAccount("Test", "User", "00210112345")
    account.balance = 200
    success = account.send_express_transfer(100)
    assert account.balance == 99
    assert success == True

  def test_personal_express_transfer_allowed_to_go_negative(self):
    account = PersonalAccount("Test", "User", "00210112345")
    account.balance = 100
    success = account.send_express_transfer(100)
    assert account.balance == -1
    assert success == True

  def test_personal_express_transfer_fail_insufficient_for_amount(self):
    account = PersonalAccount("Test", "User", "00210112345")
    account.balance = 99
    failure = account.send_express_transfer(100)
    assert account.balance == 99
    assert failure == False


class TestBusinessAccount:
  def test_business_account_creation_valid_nip(self):
    account = BusinessAccount("Firma XYZ S.A.", "1234567890")
    assert account.company_name == "Firma XYZ S.A."
    assert account.nip == "1234567890"
    assert account.balance == 0
  def test_business_account_invalid_nip_short(self):
    account = BusinessAccount("Firma Krzak", "123")
    assert account.nip == "Invalid"

  def test_business_account_invalid_nip_long(self):
    account = BusinessAccount("Firma Długa", "1234567890123")
    assert account.nip == "Invalid"

  def test_business_account_invalid_nip_type(self):
    account = BusinessAccount("Firma Błąd", 1234567890)
    assert account.nip == "Invalid"

  def test_business_account_no_promo_applied(self):
    account = BusinessAccount("Firma Promocyjna", "0987654321")
    assert account.balance == 0

        
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