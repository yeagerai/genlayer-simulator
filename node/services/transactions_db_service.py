# consensus/services/transactions_db_service.py

import json

from database.db_client import DBClient


class TransactionsDBService:
    def __init__(self, db_client: DBClient):
        self.db_client = db_client
        self.db_state_table = "transactions"
        self.db_audits_table = "transactions_audit"

    def insert_transaction(
        self, from_address: str, to_address: str, data: dict, value: float, type: int
    ) -> None:
        # Insert transaction into the transactions table
        new_transaction = {
            "from_address": from_address,
            "to_address": to_address,
            "data": json.dumps(data),
            "value": value,
            "type": type,
        }
        transaction_id = self.db_client.insert(
            self.db_state_table, new_transaction, return_column="id"
        )

        # Insert transaction audit record into the transactions_audit table
        transaction_audit_record = {
            transaction_id: transaction_id,
            data: json.dumps(new_transaction),
        }
        self.db_client.insert(self.db_audits_table, transaction_audit_record)
