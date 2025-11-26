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


class TestBusinessAccountLoans:

  @pytest.mark.parametrize("balance, history, loan_amount, expected_result", [
    (5000, [-1775], 2000, True),
    (5000, [-100, -200], 2000, False),
    (1000, [-1775], 2000, False),
    (3550, [-1775, -100], 1775, True),
    (10000, [-500, -1775, -50], 1000, True),
    (5000, [-1775], -100, False),
  ])
  def test_business_loan_conditions(self, business_account, balance, history, loan_amount, expected_result):
    business_account.balance = balance
    business_account.history = history
    
    result = business_account.take_loan(loan_amount)
    
    assert result == expected_result
    
    if expected_result:
      assert business_account.balance == balance + loan_amount
    else:
      assert business_account.balance == balance