# consensus/services/state_db_service.py

import json


class StateDBService:
    def __init__(self, db_client):
        self.db_client = db_client
        self.db_state_table = "current_state"

    def get_account_by_address(self, account_address: str) -> dict:
        condition = f"id = {account_address}"
        result = self.db_client.get(self.db_state_table, condition)
        if (result[0]):
            return {
                "id": result[0]["id"],
                "balance": json.loads(result[0]["data"])["balance"],
            }
        return None

    def create_new_account(self, account_data: dict) -> None:
        account_state = {
            "id": account_data["id"],
            "data": json.dumps({"balance": account_data["balance"]}),
        }
        self.db_client.insert("current_state", account_state)

    def update_account(self, account_data: dict) -> None:
        update_condition = f"id = {account_data["id"]}"
        account_state = {
            "data": json.dumps({"balance": account_data["balance"]}),
        }
        self.db_client.update("current_State", account_state, update_condition)
