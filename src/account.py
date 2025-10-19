class Account:
	def __init__(self, first_name, last_name, pesel, promo_code = None):
		self.first_name = first_name
		self.last_name = last_name
		self.balance = 0
		self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"

		if (promo_code and promo_code.startswith("PROM_") and self.is_pesel_valid(pesel)and self.is_eligible_for_promo()):
			self.balance += 50

	def is_pesel_valid(self, pesel):
		return isinstance(pesel, str) and len(pesel) == 11
	
	def get_birth_year_from_pesel(self):
		if not self.is_pesel_valid(self.pesel):
			return None
		year = int(self.pesel[0:2])
		month = int(self.pesel[2:4])

		if 1 <= month <= 12:
			year += 1900
		elif 21 <= month <= 32:
			year += 2000
		return year

	def is_eligible_for_promo(self):
		year = self.get_birth_year_from_pesel()
		return year is not None and year > 1960