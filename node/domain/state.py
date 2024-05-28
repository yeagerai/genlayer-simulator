# consensus/domain/state.py

import json

from node.services.state_db_service import StateDBService
from node.services.transactions_db_service import TransactionsDBService
from node.errors import AccountNotFoundError, InsufficientFundsError


class State:
    def __init__(
        self,
        state_db_service: StateDBService,
        transactions_db_service: TransactionsDBService,
    ):
        self.state_db_service = state_db_service
        self.transactions_db_service = transactions_db_service

    def create_account(self, account_address: str):
        self.state_db_service.create_new_account({"id": account_address, "balance": 0})

    def fund_account(self, account_address: str, amount: int):
        # account creation or balance update
        account_data = self.state_db_service.get_account_by_address(account_address)
        if account_data:
            # Account exists, update it
            account_data["balance"] + amount
            self.state_db_service.update_account(account_data)
        else:
            # Account doesn't exist, create it
            self.state_db_service.create_new_account(
                {"id": account_address, "balance": amount}
            )

        # Record transaction
        transaction_data = {
            "from_address": "NULL",
            "to_address": account_address,
            "data": json.dumps({"action": "fund_account", "amount": amount}),
            "value": amount,
            "type": 0,
        }
        self.transactions_db_service.insert_transaction(**transaction_data)

    def send_funds(self, from_address: str, to_address: str, amount: int):
        # account fetching and validation
        from_account_data = self.state_db_service.get_account_by_address(from_address)
        to_account_data = self.state_db_service.get_account_by_address(to_address)

        if not from_account_data:
            raise AccountNotFoundError(
                from_address, f"Account {from_address} does not exist."
            )
        if not to_account_data:
            raise AccountNotFoundError(
                to_address, f"Account {to_address} does not exist."
            )
        if from_account_data["balance"] < amount:
            raise InsufficientFundsError(
                from_address, f"Insufficient funds in account {from_address}."
            )

        # Update account balances
        from_account_data["balance"] -= amount
        to_account_data["balance"] += amount
        self.state_db_service.update_account(from_account_data)
        self.state_db_service.update_account(to_account_data)

        # Record transaction
        transaction_data = {
            "from_address": from_address,
            "to_address": to_address,
            "data": json.dumps({"action": "send_funds", "amount": amount}),
            "value": amount,
            "type": 1,
        }
        self.transactions_db_service.insert_transaction(**transaction_data)
