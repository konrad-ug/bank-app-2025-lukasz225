from src.account import Account

class TestAccount:
	def test_account_creation(self):
		account = Account("John", "Doe", "02340174842")
		assert account.first_name == "John"
		assert account.last_name == "Doe"
		assert account.balance == 0
		assert account.pesel == '02340174842'

	def test_pesel_too_short(self):
		account = Account("Jane", "Doe", '123')
		assert account.pesel == "Invalid"

	def test_pesel_too_long(self):
		account = Account("Jane", "Doe", '123123123123')
		assert account.pesel == "Invalid"

	def test_pesel_is_none(self):
		account = Account("Jane", "Doe", None)
		assert account.pesel == "Invalid"

	def test_pesel_is_boolean(self):
		account = Account("Jane", "Doe",  True)
		assert account.pesel == "Invalid"


	def test_account_with_valid_promo_code(self):
		account = Account("Adam", "Nowak", "02340174842", promo_code="PROM_XYZ")
		assert account.balance == 50