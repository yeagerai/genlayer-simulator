# consensus/services/transactions_db_service.py

import json
from enum import Enum
from eth_account import Account
from eth_account._utils.validation import is_valid_address

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

    def _parse_account_data(self, account_data: dict) -> dict:
        return {
            "id": account_data["id"],
            "data": account_data["data"],
            "updated_at": account_data["updated_at"].isoformat(),
        }

    def create_new_account(self, balance: int) -> Account:
        account = Account.create()
        self.register_new_account(account.address, balance)
        return account

    def is_valid_address(address: str) -> bool:
        return is_valid_address(address)

    def get_account(self, account_address: str):
        """Private method to retrieve if an account from the data base"""
        condition = f"id = '{account_address}'"
        account_data = self.db_client.get(self.db_accounts_table, condition)
        return self._parse_account_data(account_data[0]) if account_data else None

    def get_account_or_fail(self, account_address: str):
        """Private method to check if an account exists, and raise an error if not."""
        account_data = self.get_account(account_address)
        if not account_data:
            raise AccountNotFoundError(
                account_address, f"Account {account_address} does not exist."
            )
        return account_data

    def register_new_account(self, address: str, balance: int) -> None:
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
