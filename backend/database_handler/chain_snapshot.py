# database_handler/chain_snapshot.py

from backend.database_handler.db_client import DBClient
from backend.database_handler.transactions_processor import TransactionStatus
from backend.database_handler.validators_registry import ValidatorsRegistry


class ChainSnapshot:
    def __init__(self, dbclient: DBClient):
        self.dbclient = dbclient
        self.validators_registry = ValidatorsRegistry(dbclient.engine)
        self.db_transactions_table = "transactions"
        self.pending_transactions = self._load_pending_transactions()
        self.all_validators = self._load_all_validators()
        self.num_validators = len(self.all_validators)

    def _parse_transaction_data(self, transaction_data: dict) -> dict:
        return {
            "id": transaction_data["id"],
            "status": transaction_data["status"],
            "from_address": transaction_data["from_address"],
            "to_address": transaction_data["to_address"],
            "data": transaction_data["data"],
            "consensus_data": transaction_data["consensus_data"],
            "nonce": transaction_data["nonce"],
            "value": float(transaction_data["value"]),
            "type": transaction_data["type"],
            "gaslimit": transaction_data["gaslimit"],
            "created_at": transaction_data["created_at"].isoformat(),
            "r": transaction_data["r"],
            "v": transaction_data["v"],
        }

    def _load_pending_transactions(self):
        """Load and return the list of pending transactions from the database."""
        pending_transactions = self.dbclient.get(
            self.db_transactions_table, f"status = '{TransactionStatus.PENDING.value}'"
        )
        return [
            self._parse_transaction_data(transaction)
            for transaction in pending_transactions
        ]

    def _load_all_validators(self):
        """Load and return the list of all validators from the database."""
        return self.validators_registry.get_all_validators()

    def get_pending_transactions(self):
        """Return the list of pending transactions."""
        return self.pending_transactions

    def get_all_validators(self):
        """Return the list of all validators."""
        return self.all_validators
