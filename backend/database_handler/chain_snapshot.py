# database_handler/chain_snapshot.py

from backend.database_handler.db_client import DBClient


class ChainSnapshot:
    def __init__(self, dbclient: DBClient):
        self.dbclient = dbclient
        self.db_transactions_table = "transactions"
        self.db_validators_table = "validators"
        self.pending_transactions = self._load_pending_transactions()
        self.all_validators = self._load_all_validators()
        self.num_validators = len(self.all_validators)

    def _load_pending_transactions(self):
        """Load and return the list of pending transactions from the database."""
        return self.dbclient.get(self.db_transactions_table, "status = 'PENDING'")

    def _load_all_validators(self):
        """Load and return the list of all validators from the database."""
        return self.dbclient.get(self.db_validators_table)

    def get_pending_transactions(self):
        """Return the list of pending transactions."""
        return self.pending_transactions

    def get_all_validators(self):
        """Return the list of all validators."""
        return self.all_validators
