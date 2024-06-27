# database_handler/contract_snapshot.py
import json
from backend.database_handler.db_client import DBClient


class ContractSnapshot:
    def __init__(self, contract_address: str, dbclient: DBClient):
        self.dbclient = dbclient
        self.db_state_table = "current_state"
        self.db_transactions_table = "transactions"

        if not contract_address is None:
            self.contract_address = contract_address

            contract_account = self._load_contract_account()
            self.contract_data = contract_account["data"]
            self.contract_code = self.contract_data["code"]
            self.encoded_state = self.contract_data["state"]

    def _load_contract_account(self):
        """Load and return the current state of the contract from the database."""
        # Use the `get` method which retrieves rows based on a condition
        result = self.dbclient.get(
            self.db_state_table, f"id = '{self.contract_address}'", limit=1
        )
        if result:
            return result[0]
        return None

    def register_contract(self, contract: dict):
        """Register a new contract in the database."""
        parsed_contract = {"id": contract["id"], "data": json.dumps(contract["data"])}
        self.dbclient.insert(self.db_state_table, parsed_contract)

    def update_contract_state(self, new_state: str):
        """Update the state of the contract in the database."""
        new_contract_nada = json.dumps(
            {
                "code": self.contract_data["code"],
                "state": new_state,
            }
        )
        self.dbclient.update(
            self.db_state_table,
            {"data": new_contract_nada},
            f"id = '{self.contract_address}'",
        )
