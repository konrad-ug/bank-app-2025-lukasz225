import unittest
from unittest.mock import MagicMock, patch
from src.mongo_repository import MongoAccountsRepository
from src.account import Account

class TestMongoRepository(unittest.TestCase):
  def setUp(self):
    self.mock_client = MagicMock()
    self.mock_db = MagicMock()
    self.mock_collection = MagicMock()
    
    self.mock_client.__getitem__.return_value = self.mock_db
    self.mock_db.__getitem__.return_value = self.mock_collection

    with patch('src.mongo_repository.MongoClient', return_value=self.mock_client):
      self.repo = MongoAccountsRepository()

  def test_save_all(self):
    acc1 = Account("Jan", "Kowalski", "12345678901")
    accounts = [acc1]

    self.repo.save_all(accounts)

    self.repo._collection.delete_many.assert_called_once_with({})
    self.repo._collection.insert_one.assert_called()
    args, _ = self.repo._collection.insert_one.call_args
    self.assertEqual(args[0]['pesel'], "12345678901")

  def test_load_all(self):
    fake_db_data = [{
      "name": "Adam", 
      "surname": "Nowak", 
      "pesel": "98765432101", 
      "balance": 100, 
      "history": []
    }]
    self.repo._collection.find.return_value = fake_db_data

    loaded = self.repo.load_all()

    self.assertEqual(len(loaded), 1)
    self.assertEqual(loaded[0].name, "Adam")
    self.assertEqual(loaded[0].balance, 100)