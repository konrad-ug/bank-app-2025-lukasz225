from pymongo import MongoClient
from src.account import PersonalAccount

class MongoAccountsRepository:
  def __init__(self):
    self.client = MongoClient('localhost', 27017)
    self.db = self.client['bank_database']
    self._collection = self.db['accounts']

  def save_all(self, accounts):
    self._collection.delete_many({})
    for account in accounts:
      data_to_save = {
        "name": account.first_name, 
        "surname": account.last_name,
        "pesel": account.pesel,
        "balance": account.balance,
        "history": getattr(account, "history", []) 
      }
      self._collection.insert_one(data_to_save)

  def load_all(self):
    documents = self._collection.find()
    loaded_accounts = []
    for doc in documents:
      acc = PersonalAccount(doc["name"], doc["surname"], doc["pesel"])
      acc.balance = doc["balance"]
      if "history" in doc:
        acc.history = doc["history"]
      loaded_accounts.append(acc)
    return loaded_accounts