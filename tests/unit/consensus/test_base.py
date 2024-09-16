from collections import defaultdict
import pytest
from backend.consensus.base import ConsensusAlgorithm
from backend.database_handler.models import TransactionStatus
from backend.domain.types import Transaction, TransactionType


class AccountsManagerMock:
    def __init__(self, accounts: dict[str, int] | None = None):
        self.accounts = accounts or defaultdict(int)

    def get_account_balance(self, address: str) -> int:
        return self.accounts[address]

    def update_account_balance(self, address: str, balance: int):
        self.accounts[address] = balance


class TransactionsProcessorMock:
    def __init__(self, transactions=None):
        self.transactions = transactions or []

    def get_transaction_by_id(self, transaction_id: str) -> dict:
        for transaction in self.transactions:
            if transaction["id"] == transaction_id:
                return transaction
        raise ValueError(f"Transaction with id {transaction_id} not found")

    def update_transaction_status(self, transaction_id: str, status: TransactionStatus):
        self.get_transaction_by_id(transaction_id)["status"] = status

    def set_transaction_result(self, transaction_id: str, consensus_data: dict):
        self.get_transaction_by_id(transaction_id)["consensus_data"] = consensus_data


class SnapshotMock:
    def __init__(self, nodes):
        self.nodes = nodes

    def get_all_validators(self):
        return self.nodes


@pytest.mark.asyncio
async def test_exec_transaction():

    def contract_snapshot_factory(address: str):
        return None

    transaction = Transaction(
        id="transaction_id",
        from_address="from_address",
        to_address="to_address",
        status=TransactionStatus.PENDING,
        type=TransactionType.RUN_CONTRACT,
    )

    nodes = [
        {
            "address": "address1",
            "stake": 1,
            "provider": "provider1",
            "model": "model1",
            "config": "config1",
        },
        {
            "address": "address2",
            "stake": 2,
            "provider": "provider2",
            "model": "model2",
            "config": "config2",
        },
        {
            "address": "address3",
            "stake": 3,
            "provider": "provider3",
            "model": "model3",
            "config": "config3",
        },
    ]

    await ConsensusAlgorithm(None, None).exec_transaction(
        transaction=transaction,
        transactions_processor=TransactionsProcessorMock([transaction.__dict__]),
        snapshot=SnapshotMock(nodes),
        accounts_manager=AccountsManagerMock(),
        contract_snapshot_factory=contract_snapshot_factory,
    )
