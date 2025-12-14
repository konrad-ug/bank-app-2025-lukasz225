import pytest
from src.registry import AccountRegistry
from src.account import PersonalAccount

class TestAccountRegistry:

  @pytest.fixture
  def registry(self):
    return AccountRegistry()

  @pytest.fixture
  def personal_account(self):
    return PersonalAccount("Jan", "Kowalski", "90010112345")

  def test_registry_initially_empty(self, registry):
    assert registry.count() == 0
    assert registry.get_all_accounts() == []

  def test_add_account(self, registry, personal_account):
    registry.add_account(personal_account)
    
    assert registry.count() == 1
    assert registry.get_all_accounts() == [personal_account]

  def test_get_account_by_pesel(self, registry, personal_account):
    registry.add_account(personal_account)
    
    found_account = registry.get_account_by_pesel("90010112345")
    
    assert found_account == personal_account
    assert found_account.first_name == "Jan"

  def test_get_account_by_pesel_not_found(self, registry):
    found_account = registry.get_account_by_pesel("00000000000")
    
    assert found_account is None

  def test_registry_stores_multiple_accounts(self, registry):
    acc1 = PersonalAccount("A", "A", "90010112345")
    acc2 = PersonalAccount("B", "B", "90010154321")
    
    registry.add_account(acc1)
    registry.add_account(acc2)
    
    assert registry.count() == 2
    assert registry.get_account_by_pesel("90010154321") == acc2

  def test_delete_account_success(self, registry, personal_account):
    registry.add_account(personal_account)
    result = registry.delete_account(personal_account.pesel)
    assert result is True
    assert registry.count() == 0

  def test_delete_account_failed(self, registry):
    result = registry.delete_account("00000000000")
    assert result is False