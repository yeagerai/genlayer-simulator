# consensus/services/transactions_db_service.py

from .models import Transactions, TransactionsAudit
from sqlalchemy.orm import Session

from .models import TransactionStatus


class TransactionsProcessor:
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def _parse_transaction_data(transaction_data: Transactions) -> dict:
        return {
            "id": transaction_data.id,
            "from_address": transaction_data.from_address,
            "to_address": transaction_data.to_address,
            "data": transaction_data.data,
            "value": float(transaction_data.value),
            "type": transaction_data.type,
            "status": transaction_data.status.value,
            "consensus_data": transaction_data.consensus_data,
            "gaslimit": transaction_data.nonce,
            "nonce": transaction_data.nonce,
            "r": transaction_data.r,
            "s": transaction_data.s,
            "v": transaction_data.v,
            "created_at": transaction_data.created_at.isoformat(),
        }

    def insert_transaction(
        self,
        from_address: str,
        to_address: str,
        data: dict,
        value: float,
        type: int,
    ) -> int:
        # Insert transaction into the transactions table
        new_transaction = Transactions(
            from_address=from_address,
            to_address=to_address,
            data=data,
            value=value,
            type=type,
            status=TransactionStatus.PENDING,
            consensus_data=None,  # Will be set when the transaction is finalized
            # Future fields, unused for now
            gaslimit=None,
            input_data=None,
            nonce=None,
            r=None,
            s=None,
            v=None,
        )

        self.session.add(new_transaction)

        self.session.flush()  # SQLAlchemy will populate all the fields that are set by the database, like the id and created_at fields

        # Insert transaction audit record into the transactions_audit table
        transaction_audit_record = TransactionsAudit(
            transaction_id=new_transaction.id,
            data=self._parse_transaction_data(new_transaction),
        )

        self.session.add(transaction_audit_record)

        self.session.commit()

        return new_transaction.id

    def get_transaction_by_id(self, transaction_id: int) -> dict | None:
        transaction = (
            self.session.query(Transactions).filter_by(id=transaction_id).one_or_none()
        )

        if transaction is None:
            return None

        return self._parse_transaction_data(transaction)

    def update_transaction_status(
        self, transaction_id: int, new_status: TransactionStatus
    ):

        transaction = (
            self.session.query(Transactions).filter_by(id=transaction_id).one()
        )

        transaction.status = new_status
        self.session.commit()

    def set_transaction_result(self, transaction_id: int, consensus_data: dict):
        transaction = (
            self.session.query(Transactions).filter_by(id=transaction_id).one()
        )

        transaction.status = TransactionStatus.FINALIZED
        transaction.consensus_data = consensus_data

        print(
            "Updating transaction status",
            transaction_id,
            TransactionStatus.FINALIZED.value,
        )
        self.session.commit()
