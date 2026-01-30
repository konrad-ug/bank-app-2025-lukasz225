import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from src.registry import AccountRegistry
from src.account import PersonalAccount
from src.mongo_repository import MongoAccountsRepository

app = Flask(__name__)
registry = AccountRegistry()
account_repository = MongoAccountsRepository()

@app.route("/api/accounts", methods=['POST'])
def create_account():
  data = request.get_json()
  print(f"Request create account: {data}")

  name = data.get("name")
  surname = data.get("surname")
  pesel = data.get("pesel")

  if registry.get_account_by_pesel(pesel):
    return jsonify({"message": "Account with this pesel already exists"}), 409

  account = PersonalAccount(name, surname, pesel)
  registry.add_account(account)
  return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
  print("Request get all accounts")
  accounts = registry.get_all_accounts()
  accounts_data = [
    {"name": acc.first_name, "surname": acc.last_name, "pesel": acc.pesel, "balance": acc.balance} 
    for acc in accounts
  ]
  return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
  print("Request get account count")
  count = registry.count()
  return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
  print(f"Request get account by pesel: {pesel}")
  account = registry.get_account_by_pesel(pesel)
  
  if not account:
    return jsonify({"message": "Account not found"}), 404
  
  return jsonify({
    "name": account.first_name, 
    "surname": account.last_name, 
    "pesel": account.pesel, 
    "balance": account.balance
  }), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
  print(f"Request update account: {pesel}")
  data = request.get_json()
  account = registry.get_account_by_pesel(pesel)
  
  if not account:
    return jsonify({"message": "Account not found"}), 404
  
  if "name" in data:
    account.first_name = data["name"]
  if "surname" in data:
    account.last_name = data["surname"]
    
  return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
  print(f"Request delete account: {pesel}")
  success = registry.delete_account(pesel)
  
  if not success:
    return jsonify({"message": "Account not found"}), 404
    
  return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer_money(pesel):
  data = request.get_json()
  amount = data.get("amount")
  transfer_type = data.get("type")
  
  print(f"Request transfer: pesel={pesel}, amount={amount}, type={transfer_type}")

  account = registry.get_account_by_pesel(pesel)

  if not account:
    return jsonify({"message": "Account not found"}), 404

  if transfer_type == "incoming":
    account.receive_transfer(amount)
    return jsonify({"message": "Transfer accepted"}), 200
  
  elif transfer_type == "outgoing":
    success = account.send_transfer(amount)
    if success:
      return jsonify({"message": "Transfer accepted"}), 200
    else:
      return jsonify({"message": "Transfer failed"}), 422
      
  elif transfer_type == "express":
    success = account.send_express_transfer(amount)
    if success:
      return jsonify({"message": "Transfer accepted"}), 200
    else:
      return jsonify({"message": "Transfer failed"}), 422
  
  else:
    return jsonify({"message": "Unknown transfer type"}), 400

@app.route("/api/accounts/save", methods=['POST'])
def save_accounts():
  print("Request save accounts to DB")
  current_accounts = registry.get_all_accounts()
  account_repository.save_all(current_accounts)
  return jsonify({"message": "Accounts saved successfully"}), 200

@app.route("/api/accounts/load", methods=['POST'])
def load_accounts():
  print("Request load accounts from DB")
  registry.accounts = [] 
  
  loaded_accounts = account_repository.load_all()
  for acc in loaded_accounts:
    registry.add_account(acc)
    
  return jsonify({"message": "Accounts loaded successfully", "count": len(loaded_accounts)}), 200

if __name__ == '__main__':
  app.run(debug=True)