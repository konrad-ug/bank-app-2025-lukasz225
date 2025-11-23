import pytest
from src.account import PersonalAccount, BusinessAccount

class TestPersonalAccountLoans:

  @pytest.mark.parametrize("transactions, loan_amount, expected_balance", [
    ([100, 200, 300], 5000, 5600),
    ([1000, 1000, 1000, -500, 100], 2500, 5100),
    ([1000, 1000, 1000, 100, 100], 2000, 5200),
  ])
  def test_loan_granted(self, personal_account, transactions, loan_amount, expected_balance):
    for t in transactions:
      if t > 0:
        personal_account.receive_transfer(t)
      else:
        if personal_account.balance < abs(t):
          personal_account.balance += abs(t) 
        personal_account.send_transfer(abs(t))

    is_granted = personal_account.submit_for_loan(loan_amount)

    assert is_granted is True
    assert personal_account.balance == expected_balance


  @pytest.mark.parametrize("transactions, loan_amount", [
    ([], 1000),
    ([100, 100], 1000),
    ([100, 200, -50], 5000),
    ([1000, 1000, 1000, -500, 100], 3000),
    ([100, 100, 100], -500),
  ])
  def test_loan_denied(self, personal_account, transactions, loan_amount):
    for t in transactions:
      if t > 0:
        personal_account.receive_transfer(t)
      else:
        personal_account.balance += abs(t)
        personal_account.send_transfer(abs(t))
    
    current_balance = personal_account.balance 

    is_granted = personal_account.submit_for_loan(loan_amount)

    assert is_granted is False
    assert personal_account.balance == current_balance

  def test_business_account_cannot_take_loan(self, business_account):
    with pytest.raises(AttributeError):
      business_account.submit_for_loan(1000)