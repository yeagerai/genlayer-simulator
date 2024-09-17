from collections import defaultdict
import pytest
from backend.consensus.base import ConsensusAlgorithm
from backend.database_handler.contract_snapshot import ContractSnapshot
from backend.database_handler.models import TransactionStatus
from backend.domain.types import Transaction, TransactionType
from backend.node.genvm.types import ExecutionMode, ExecutionResultStatus, Receipt, Vote
from backend.protocol_rpc.message_handler.base import MessageHandler


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


def transaction_to_dict(transaction: Transaction) -> dict:
    return {
        "id": transaction.id,
        "status": transaction.status.value,
        "from_address": transaction.from_address,
        "to_address": transaction.to_address,
        "input_data": transaction.input_data,
        "data": transaction.data,
        "consensus_data": transaction.consensus_data,
        "nonce": transaction.nonce,
        "value": transaction.value,
        "type": transaction.type.value,
        "gaslimit": transaction.gaslimit,
        "r": transaction.r,
        "s": transaction.s,
        "v": transaction.v,
    }


@pytest.mark.asyncio
async def test_exec_transaction():

    def contract_snapshot_factory(address: str):
        class ContractSnapshotMock:
            def __init__(self):
                self.address = address

            def update_contract_state(self, state: str):
                pass

        return ContractSnapshotMock()

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

    def node_factory(
        node: dict,
        mode: ExecutionMode,
        contract_snapshot: ContractSnapshot,
        receipt: Receipt | None,
        msg_handler: MessageHandler,
    ):

        class NodeMock:
            def __init__(self):
                self.validator_mode = mode
                self.address = node["address"]
                self.leader_receipt = receipt

            async def exec_transaction(self, transaction: Transaction) -> Receipt:
                return Receipt(
                    vote=Vote.AGREE,
                    class_name="",
                    args=[],
                    mode=mode,
                    method="",
                    gas_used=0,
                    contract_state="",
                    node_config={},
                    eq_outputs={},
                    execution_result=ExecutionResultStatus.SUCCESS,
                    error=None,
                )

        return NodeMock()

    await ConsensusAlgorithm(None, None).exec_transaction(
        transaction=transaction,
        transactions_processor=TransactionsProcessorMock(
            [transaction_to_dict(transaction)]
        ),
        snapshot=SnapshotMock(nodes),
        accounts_manager=AccountsManagerMock(),
        contract_snapshot_factory=contract_snapshot_factory,
        node_factory=node_factory,
    )
