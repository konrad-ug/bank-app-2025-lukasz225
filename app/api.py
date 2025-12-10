import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from src.registry import AccountRegistry
from src.account import PersonalAccount

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Request create account: {data}")

    name = data.get("name")
    surname = data.get("surname")
    pesel = data.get("pesel")

    if registry.get_account_by_pesel(pesel):
        return jsonify({"message": "Account with this pesel already exists"}), 400

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

if __name__ == '__main__':
    app.run(debug=True)