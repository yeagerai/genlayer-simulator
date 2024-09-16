from collections import defaultdict
import pytest
from backend.consensus.base import ConsensusAlgorithm


class AccountsManagerMock:
    def __init__(self):
        self.accounts = defaultdict(int)

    def get_account_balance(self, address) -> int:
        return self.accounts[address]

    def update_account_balance(self, address, balance):
        self.accounts[address] = balance


class TransactionsProcessorMock:
    def __init__(self):
        self.transactions = {}

    def get_transaction_by_id(self, transaction_id) -> dict | None:
        return self.transactions.get(transaction_id)

    def update_transaction_status(self, transaction_id, status):
        self.transactions[transaction_id]["status"] = status

    def set_transaction_result(self, transaction_id, consensus_data):
        self.transactions[transaction_id]["consensus_data"] = consensus_data


class SnapshotMock:
    def __init__(self, nodes):
        self.nodes = nodes

    def get_all_validators(self):
        return self.nodes


@pytest.mark.asyncio
async def test_exec_transaction():

    def contract_snapshot_factory():
        pass

    await ConsensusAlgorithm(None, None).exec_transaction(
        transaction={},
        transactions_processor=TransactionsProcessorMock(),
        snapshot=None,
        accounts_manager=AccountsManagerMock(),
        contract_snapshot_factory=contract_snapshot_factory,
    )
