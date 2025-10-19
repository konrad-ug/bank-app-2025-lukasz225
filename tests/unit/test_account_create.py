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


	def test_account_with_valid_promo_code_and_pesel(self):
		account = Account("Jane", "Doe", "02320174842", promo_code="PROM_XYZ")
		assert account.balance == 50

	def test_promo_given_if_born_after_1960(self):
		account = Account("Jane", "Doe", "02320174842", promo_code="PROM_ABC")
		assert account.balance == 50

	def test_no_promo_if_born_before_1960(self):
		account = Account("Jane", "Doe", "59010112345", promo_code="PROM_ABC")
		assert account.balance == 0

	def test_no_promo_if_pesel_invalid(self):
		account = Account("Jane", "Doe", "123", promo_code="PROM_ABC")
		assert account.balance == 0

	def test_no_promo_if_code_invalid(self):
		account = Account("Jane", "Doe", "02340174842", promo_code="XYZ")
		assert account.balance == 0
