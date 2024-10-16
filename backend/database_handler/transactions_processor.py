# consensus/services/transactions_db_service.py
import rlp

from .models import Transactions, TransactionsAudit
from sqlalchemy.orm import Session
from sqlalchemy import or_

from .models import TransactionStatus
from eth_utils import to_bytes, keccak, is_address
import json


class TransactionsProcessor:
    def __init__(
        self,
        session: Session,
    ):
        self.session = session

    @staticmethod
    def _parse_transaction_data(transaction_data: Transactions) -> dict:
        return {
            "hash": transaction_data.hash,
            "from_address": transaction_data.from_address,
            "to_address": transaction_data.to_address,
            "data": transaction_data.data,
            "value": transaction_data.value,
            "type": transaction_data.type,
            "status": transaction_data.status.value,
            "consensus_data": transaction_data.consensus_data,
            "gaslimit": transaction_data.nonce,
            "nonce": transaction_data.nonce,
            "r": transaction_data.r,
            "s": transaction_data.s,
            "v": transaction_data.v,
            "created_at": transaction_data.created_at.isoformat(),
            "leader_only": transaction_data.leader_only,
            "client_session_id": transaction_data.client_session_id,
            "triggered_by": transaction_data.triggered_by_hash,
            "triggered_transactions": [
                transaction.hash
                for transaction in transaction_data.triggered_transactions
            ],
        }

    @staticmethod
    def _generate_transaction_hash(
        from_address: str,
        to_address: str,
        data: dict,
        value: float,
        type: int,
        nonce: int,
    ) -> str:
        from_address_bytes = (
            to_bytes(hexstr=from_address) if is_address(from_address) else None
        )
        to_address_bytes = (
            to_bytes(hexstr=to_address) if is_address(to_address) else None
        )
        data_bytes = to_bytes(text=json.dumps(data))

        tx_elements = [
            from_address_bytes,
            to_address_bytes,
            to_bytes(hexstr=hex(int(value))),
            data_bytes,
            to_bytes(hexstr=hex(type)),
            to_bytes(hexstr=hex(nonce)),
            to_bytes(hexstr=hex(0)),  # gas price (placeholder)
            to_bytes(hexstr=hex(0)),  # gas limit (placeholder)
        ]

        # Filter out None values
        tx_elements = [elem for elem in tx_elements if elem is not None]
        rlp_encoded = rlp.encode(tx_elements)
        hash = "0x" + keccak(rlp_encoded).hex()
        return hash

    def insert_transaction(
        self,
        from_address: str,
        to_address: str,
        data: dict,
        value: float,
        type: int,
        nonce: int,
        leader_only: bool,
        client_session_id: str | None,
        triggered_by_hash: (
            str | None
        ) = None,  # If filled, the transaction must be present in the database (committed)
    ) -> str:
        current_nonce = self.get_transaction_count(from_address)

        if nonce != current_nonce:
            raise Exception(
                f"Unexpected nonce. Provided: {nonce}, expected: {current_nonce}"
            )

        transaction_hash = self._generate_transaction_hash(
            from_address, to_address, data, value, type, nonce
        )

        new_transaction = Transactions(
            hash=transaction_hash,
            from_address=from_address,
            to_address=to_address,
            data=data,
            value=value,
            type=type,
            status=TransactionStatus.PENDING,
            consensus_data=None,  # Will be set when the transaction is finalized
            nonce=nonce,
            # Future fields, unused for now
            gaslimit=None,
            input_data=None,
            r=None,
            s=None,
            v=None,
            leader_only=leader_only,
            client_session_id=client_session_id,
            triggered_by=(
                self.session.query(Transactions).filter_by(hash=triggered_by_hash).one()
                if triggered_by_hash
                else None
            ),
        )

        self.session.add(new_transaction)

        self.session.flush()  # So that `created_at` gets set

        transaction_audit_record = TransactionsAudit(
            transaction_hash=new_transaction.hash,
            data=self._parse_transaction_data(new_transaction),
        )

        self.session.add(transaction_audit_record)

        return new_transaction.hash

    def get_transaction_by_hash(self, transaction_hash: str) -> dict | None:
        transaction = (
            self.session.query(Transactions)
            .filter_by(hash=transaction_hash)
            .one_or_none()
        )

        if transaction is None:
            return None

        return self._parse_transaction_data(transaction)

    def update_transaction_status(
        self, transaction_hash: str, new_status: TransactionStatus
    ):

        transaction = (
            self.session.query(Transactions).filter_by(hash=transaction_hash).one()
        )

        transaction.status = new_status

    def set_transaction_result(self, transaction_hash: str, consensus_data: dict):
        transaction = (
            self.session.query(Transactions).filter_by(hash=transaction_hash).one()
        )

        transaction.status = TransactionStatus.FINALIZED
        transaction.consensus_data = consensus_data

        print(
            "Updating transaction status",
            transaction_hash,
            TransactionStatus.FINALIZED.value,
        )

    def get_transaction_count(self, address: str) -> int:
        count = (
            self.session.query(Transactions)
            .filter(Transactions.from_address == address)
            .count()
        )
        return count

    def get_transactions_for_address(self, address: str) -> list[dict]:
        transactions = (
            self.session.query(Transactions)
            .filter(
                or_(
                    Transactions.from_address == address,
                    Transactions.to_address == address,
                )
            )
            .order_by(Transactions.created_at.desc())
            .all()
        )

        return [
            self._parse_transaction_data(transaction) for transaction in transactions
        ]
