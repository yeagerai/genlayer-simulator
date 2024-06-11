# consensus/services/transactions_db_service.py

import json
from enum import Enum

from backend.database_handler.db_client import DBClient
from backend.database_handler.errors import AccountNotFoundError
from backend.database_handler.transactions_processor import TransactionsProcessor


class AccountsManager:
    def __init__(
        self, db_client: DBClient, transactions_processor: TransactionsProcessor
    ):
        self.db_client = db_client
        self.transactions_processor = transactions_processor
        self.db_accounts_table = "current_state"

    def get_account(self, account_address: str):
        """Private method to retrieve if an account from the data base"""
        condition = f"id = '{account_address}'"
        return self.db_client.get(self.db_accounts_table, condition)

    def get_account_or_fail(self, account_address: str):
        """Private method to check if an account exists, and raise an error if not."""
        account_data = self.get_account(account_address)
        if not account_data:
            raise AccountNotFoundError(
                account_address, f"Account {account_address} does not exist."
            )
        return account_data

    def create_new_account(self, address: str, balance: int) -> None:
        account_state = {
            "id": address,
            "data": json.dumps({"balance": balance}),
        }
        self.db_client.insert(self.db_accounts_table, account_state)

    def fund_account(self, account_address: str, amount: int):
        # account creation or balance update
        account_data = self.get_account(account_address)
        if account_data:
            # Account exists, update it
            update_condition = f"id = {account_address}"
            new_balance = account_data["data"]["balance"] + amount
            updated_account_state = {
                "data": json.dumps({"balance": new_balance}),
            }

            self.db_client.update(
                self.db_accounts_table, updated_account_state, update_condition
            )
        else:
            # Account doesn't exist, create it
            self.create_new_account(account_address, amount)

        # Record transaction
        transaction_data = {
            "from_address": "NULL",
            "to_address": account_address,
            "data": json.dumps({"action": "fund_account", "amount": amount}),
            "value": amount,
            "type": 0,
        }
        self.transactions_processor.insert_transaction(**transaction_data)
