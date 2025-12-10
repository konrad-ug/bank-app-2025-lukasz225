class AccountRegistry:
  def __init__(self):
    self.accounts = []

  def add_account(self, account):
    self.accounts.append(account)

  def count(self):
    return len(self.accounts)

  def get_all_accounts(self):
    return self.accounts

  def get_account_by_pesel(self, pesel):
    for account in self.accounts:
      if account.pesel == pesel:
        return account
    return None

  def delete_account(self, pesel):
    account_to_delete = self.get_account_by_pesel(pesel)
    if account_to_delete:
      self.accounts.remove(account_to_delete)
      return True
    return False