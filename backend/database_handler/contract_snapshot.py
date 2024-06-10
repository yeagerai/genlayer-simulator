# database_handler/contract_snapshot.py
import json
from backend.database_handler.db_client import DBClient


class ContractSnapshot:
    def __init__(self, contract_address: str, dbclient: DBClient):
        self.dbclient = dbclient
        self.db_status_table = "current_status"
        self.db_transactions_table = "transactions"
        self.contract_address = contract_address

        contract_state = self._load_contract_state()
        contract_data = json.loads(contract_state["data"])
        self.encoded_state = contract_data["state"]  # current binary state in the DB

    def _load_contract_state(self):
        """Load and return the current state of the contract from the database."""
        # Use the `get` method which retrieves rows based on a condition
        result = self.dbclient.get(
            self.db_status_table, f"id = '{self.contract_address}'", limit=1
        )
        if result:
            return result[0]["state"]
        return None

    def expire_queued_transactions(self):
        """Sets all PENDING status transactions associated with this contract to CANCELED status."""
        condition = (
            f"status = 'PENDING' AND contract_address = '{self.contract_address}'"
        )
        self.dbclient.update(
            self.db_transactions_table, {"status": "CANCELED"}, condition
        )
