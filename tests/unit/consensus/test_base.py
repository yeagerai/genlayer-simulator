from collections import defaultdict
import pytest
from backend.consensus.base import ConsensusAlgorithm
from backend.database_handler.models import TransactionStatus


class AccountsManagerMock:
    def __init__(self):
        self.accounts = defaultdict(int)

    def get_account_balance(self, address) -> int:
        return self.accounts[address]

    def update_account_balance(self, address, balance):
        self.accounts[address] = balance


class TransactionsProcessorMock:
    def __init__(self, transactions=None):
        self.transactions = transactions or []

    def get_transaction_by_id(self, transaction_id) -> dict | None:
        for transaction in self.transactions:
            if transaction["id"] == transaction_id:
                return transaction
        return None

    def update_transaction_status(self, transaction_id, status):
        self.get_transaction_by_id(transaction_id)["status"] = status

    def set_transaction_result(self, transaction_id, consensus_data):
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

    transaction = {
        "id": "transaction_id",
        "from": "from_address",
        "to": "to_address",
        "status": TransactionStatus.PENDING.value,
        "type": 1,
    }

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
        transactions_processor=TransactionsProcessorMock([transaction]),
        snapshot=SnapshotMock(nodes),
        accounts_manager=AccountsManagerMock(),
        contract_snapshot_factory=contract_snapshot_factory,
    )
