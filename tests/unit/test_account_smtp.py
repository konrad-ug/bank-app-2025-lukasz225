import pytest
from unittest.mock import patch
from datetime import datetime
from src.account import PersonalAccount, BusinessAccount
from src.smtp_client import SMTPClient

class TestAccountEmail:
  
  @patch('src.account.SMTPClient.send')
  def test_send_email_personal_account_success(self, mock_send):
    mock_send.return_value = True
    account = PersonalAccount("Jan", "Kowalski", "12345678901")
    account.history = [100, -50]
    email = "test@email.com"
    today = datetime.today().strftime('%Y-%m-%d')

    result = account.send_history_via_email(email)

    assert result is True
    mock_send.assert_called_once()
    
    args = mock_send.call_args
    assert args[0][0] == f"Account Transfer History {today}"
    assert args[0][1] == "Personal account history: [100, -50]"
    assert args[0][2] == email

  @patch('src.account.SMTPClient.send')
  def test_send_email_personal_account_failure(self, mock_send):
    mock_send.return_value = False
    account = PersonalAccount("Jan", "Kowalski", "12345678901")
    
    result = account.send_history_via_email("test@fail.com")

    assert result is False
    mock_send.assert_called_once()

  @patch('src.account.SMTPClient.send')
  @patch('src.account.BusinessAccount._validate_nip_with_gov')
  def test_send_email_business_account(self, mock_validate_nip, mock_send):
    mock_validate_nip.return_value = True
    mock_send.return_value = True
    
    account = BusinessAccount("Firma XYZ", "1234567890")
    account.history = [5000, -1000]
    email = "biznes@firma.pl"
    today = datetime.today().strftime('%Y-%m-%d')

    result = account.send_history_via_email(email)

    assert result is True
    
    args = mock_send.call_args
    assert args[0][0] == f"Account Transfer History {today}"
    assert args[0][1] == "Company account history: [5000, -1000]"
    assert args[0][2] == email

  def test_real_smtp_client_returns_false(self):
    smtp = SMTPClient()
    result = smtp.send("Temat", "Tresc", "email@test.pl")
    assert result is False