import pytest
from src.account import PersonalAccount, BusinessAccount

VALID_PESEL_NO_PROMO = "50010112345"

class TestPersonalAccountLoans:

	def test_loan_denied_empty_history(self):
		account = PersonalAccount("Jan", "Kowalski", VALID_PESEL_NO_PROMO)
		assert account.balance == 0
		
		is_granted = account.submit_for_loan(1000)
		
		assert is_granted == False
		assert account.balance == 0
		assert account.history == []

	def test_loan_denied_not_enough_transactions(self):
		account = PersonalAccount("Jan", "Kowalski", VALID_PESEL_NO_PROMO)
		account.receive_transfer(100)
		account.receive_transfer(100)
		
		is_granted = account.submit_for_loan(1000)
		
		assert is_granted == False
		assert account.balance == 200
		assert account.history == [100, 100]

	def test_loan_granted_condition_1_three_deposits(self):
		account = PersonalAccount("Jan", "Kowalski", VALID_PESEL_NO_PROMO)
		account.receive_transfer(100)
		account.receive_transfer(200)
		account.receive_transfer(300)
		
		is_granted = account.submit_for_loan(5000)
		
		assert is_granted == True
		assert account.balance == (100 + 200 + 300 + 5000)
		assert account.history == [100, 200, 300, 5000]

	def test_loan_denied_condition_1_fails_one_withdrawal(self):
		account = PersonalAccount("Jan", "Kowalski", VALID_PESEL_NO_PROMO)
		account.receive_transfer(100)
		account.receive_transfer(200)
		account.send_transfer(50)
		
		is_granted = account.submit_for_loan(5000)
		
		assert is_granted == False
		assert account.balance == (100 + 200 - 50)
		assert account.history == [100, 200, -50]

	def test_loan_granted_condition_2_sum_of_five_gt_amount(self):
		account = PersonalAccount("Jan", "Kowalski", VALID_PESEL_NO_PROMO)
		account.receive_transfer(1000)
		account.receive_transfer(1000)
		account.receive_transfer(1000)
		account.send_transfer(500)
		account.receive_transfer(100)

		is_granted = account.submit_for_loan(2500)
		
		assert is_granted == True
		assert account.balance == (2600 + 2500)
		assert account.history == [1000, 1000, 1000, -500, 100, 2500]

	def test_loan_denied_condition_2_fails_sum_of_five_lte_amount(self):
		account = PersonalAccount("Jan", "Kowalski", VALID_PESEL_NO_PROMO)
		account.receive_transfer(1000)
		account.receive_transfer(1000)
		account.receive_transfer(1000)
		account.send_transfer(500)
		account.receive_transfer(100)
		
		is_granted = account.submit_for_loan(3000)
		
		assert is_granted == False
		assert account.balance == 2600
		assert account.history == [1000, 1000, 1000, -500, 100]

	def test_loan_granted_cond1_pass_cond2_fail(self):
		account = PersonalAccount("Jan", "Kowalski", VALID_PESEL_NO_PROMO)
		account.receive_transfer(10)
		account.receive_transfer(10)
		account.receive_transfer(10)
		account.receive_transfer(10)
		account.receive_transfer(10)
		
		is_granted = account.submit_for_loan(1000)

		assert is_granted == True
		assert account.balance == (50 + 1000)

	def test_loan_granted_cond1_fail_cond2_pass(self):
		account = PersonalAccount("Jan", "Kowalski", VALID_PESEL_NO_PROMO)
		account.receive_transfer(10000)
		account.receive_transfer(10000)
		account.send_transfer(100)
		account.receive_transfer(1000)
		account.receive_transfer(1000)
		
		is_granted = account.submit_for_loan(20000)
		
		assert is_granted == True
		assert account.balance == (21900 + 20000)

	def test_loan_denied_for_negative_amount(self):
		account = PersonalAccount("Jan", "Kowalski", VALID_PESEL_NO_PROMO)
		account.receive_transfer(100)
		account.receive_transfer(100)
		account.receive_transfer(100)
		
		is_granted = account.submit_for_loan(-500)
		
		assert is_granted == False
		assert account.balance == 300

	def test_business_account_cannot_take_loan(self):
		account = BusinessAccount("Firma", "1234567890")
		with pytest.raises(AttributeError):
			account.submit_for_loan(1000)