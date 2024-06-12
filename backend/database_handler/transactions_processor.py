# consensus/services/transactions_db_service.py

import json
from enum import Enum

from backend.database_handler.db_client import DBClient


class TransactionStatus(Enum):
    PENDING = "PENDING"
    CANCELED = "CANCELED"
    PROPOSING = "PROPOSING"
    COMMITTING = "COMMITTING"
    REVEALING = "REVEALING"
    ACCEPTED = "ACCEPTED"
    FINALIZED = "FINALIZED"
    UNDETERMINED = "UNDETERMINED"


class TransactionsProcessor:
    def __init__(self, db_client: DBClient):
        self.db_client = db_client
        self.db_transactions_table = "transactions"
        self.db_audits_table = "transactions_audit"

    def insert_transaction(
        self, from_address: str, to_address: str, data: dict, value: float, type: int
    ) -> int:
        # Insert transaction into the transactions table
        new_transaction = {
            "from_address": from_address,
            "to_address": to_address,
            "data": json.dumps(data),
            "value": value,
            "type": type,
            "status": TransactionStatus.PENDING.value,
        }
        transaction_id = self.db_client.insert(
            self.db_transactions_table, new_transaction, return_column="id"
        )

        # Insert transaction audit record into the transactions_audit table
        transaction_audit_record = {
            "transaction_id": transaction_id,
            "data": json.dumps(new_transaction),
        }
        self.db_client.insert(self.db_audits_table, transaction_audit_record)

        return transaction_id

    def get_transaction_by_id(self, transaction_id: int) -> dict:
        condition = f"id = {transaction_id}"
        return self.db_client.get(self.db_transactions_table, condition)

    def update_transaction_status(
        self, transaction_id: int, new_status: TransactionStatus
    ):
        update_condition = f"id = {transaction_id}"
        update_data = {"status": new_status}
        self.db_client.update(self.db_transactions_table, update_data, update_condition)

    def set_transaction_result(self, transaction_id: int, consensus_data: dict):
        update_condition = f"id = {transaction_id}"
        update_data = {
            "status": TransactionStatus.FINALIZED.value,
            "consensus_data": json.dumps(consensus_data),
        }
        self.db_client.update(self.db_transactions_table, update_data, update_condition)
