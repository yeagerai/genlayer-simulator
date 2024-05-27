# consensus/domain/state.py

import json


class State:
    def __init__(self, state_db_service, transactions_db_service):
        self.state_db_service = state_db_service
        self.transactions_db_service = transactions_db_service

    def create_account(self, account_address):
        self.state_db_service.create_new_account({"id": account_address, "balance": 0})

    def fund_account(self, account_address, amount):
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
