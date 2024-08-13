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

    def _parse_transaction_data(self, transaction_data: dict) -> dict:
        return {
            "id": transaction_data["id"],
            "from_address": transaction_data["from_address"],
            "to_address": transaction_data["to_address"],
            "data": transaction_data["data"],
            "value": float(transaction_data["value"]),
            "type": transaction_data["type"],
            "status": transaction_data["status"],
            "consensus_data": transaction_data["consensus_data"],
            "gaslimit": transaction_data["nonce"],
            "nonce": transaction_data["nonce"],
            "r": transaction_data["r"],
            "s": transaction_data["s"],
            "v": transaction_data["v"],
            "created_at": transaction_data["created_at"].isoformat(),
        }

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
        transaction_data = self.db_client.get(self.db_transactions_table, condition)
        if len(transaction_data) == 0:
            return None
        return self._parse_transaction_data(transaction_data[0])

    def update_transaction_status(
        self, transaction_id: int, new_status: TransactionStatus
    ):
        update_condition = f"id = {transaction_id}"
        update_data = {"status": new_status}
        print("Updating transaction status", transaction_id, new_status)
        self.db_client.update(self.db_transactions_table, update_data, update_condition)

    def set_transaction_result(self, transaction_id: int, consensus_data: dict):
        update_condition = f"id = {transaction_id}"
        update_data = {
            "status": TransactionStatus.FINALIZED.value,
            "consensus_data": json.dumps(consensus_data),
        }
        print(
            "Updating transaction status",
            transaction_id,
            TransactionStatus.FINALIZED.value,
        )
        self.db_client.update(self.db_transactions_table, update_data, update_condition)
