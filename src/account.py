class Account:
  def __init__(self):
    self.balance = 0
    self.express_transfer_fee = 0
    self.history = []

  def receive_transfer(self, amount):
    if amount > 0:
      self.balance += amount
      self.history.append(amount)

  def send_transfer(self, amount):
    if amount > 0 and self.balance >= amount:
      self.balance -= amount
      self.history.append(-amount)
      return True
    else:
      return False

  def send_express_transfer(self, amount):
    if amount > 0 and self.balance >= amount:
      self.balance -= (amount + self.express_transfer_fee)
      self.history.append(-amount)
      self.history.append(-self.express_transfer_fee)
      return True
    else:
      return False


class PersonalAccount(Account):
  def __init__(self, first_name, last_name, pesel, promo_code=None):
    super().__init__()
    self.express_transfer_fee = 1
    self.first_name = first_name
    self.last_name = last_name
    self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"

    if promo_code and promo_code.startswith("PROM_") and self.is_eligible_for_promo():
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

  def _check_loan_condition_last_three_positive(self):
    if len(self.history) >= 3:
      last_three = self.history[-3:]
      return all(t > 0 for t in last_three)
    return False

  def _check_loan_condition_sum_last_five(self, amount):
    if len(self.history) >= 5:
      last_five = self.history[-5:]
      return sum(last_five) > amount
    return False

  def submit_for_loan(self, amount):
    if amount <= 0:
      return False
    
    condition1 = self._check_loan_condition_last_three_positive()
    condition2 = self._check_loan_condition_sum_last_five(amount)

    if condition1 or condition2:
      self.balance += amount
      self.history.append(amount)
      return True
    
    return False


class BusinessAccount(Account):
  def __init__(self, company_name, nip):
    super().__init__()
    self.express_transfer_fee = 5
    self.company_name = company_name
    self.nip = nip if self.is_nip_valid(nip) else "Invalid"

  def is_nip_valid(self, nip):
    return isinstance(nip, str) and len(nip) == 10