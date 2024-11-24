from collections import defaultdict
from typing import Callable, List
from unittest.mock import AsyncMock, Mock
import time
import threading
import asyncio

import pytest

from backend.consensus.base import (
    ConsensusAlgorithm,
    rotate,
    CommittingState,
    FinalizingState,
    TransactionContext,
    DEFAULT_VALIDATORS_COUNT,
)
from backend.database_handler.contract_snapshot import ContractSnapshot
from backend.database_handler.models import TransactionStatus
from backend.domain.types import Transaction, TransactionType
from backend.node.base import Node
from backend.node.genvm.types import ExecutionMode, ExecutionResultStatus, Receipt, Vote
from backend.protocol_rpc.message_handler.base import MessageHandler

DEFAULT_FINALITY_WINDOW = 5


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
        self.updated_transaction_status_history = defaultdict(list)

    def get_transaction_by_hash(self, transaction_hash: str) -> dict:
        for transaction in self.transactions:
            if transaction["hash"] == transaction_hash:
                return transaction
        raise ValueError(f"Transaction with hash {transaction_hash} not found")

    def update_transaction_status(
        self, transaction_hash: str, status: TransactionStatus
    ):
        self.get_transaction_by_hash(transaction_hash)["status"] = status.value
        self.updated_transaction_status_history[transaction_hash].append(status)

    def set_transaction_result(self, transaction_hash: str, consensus_data: dict):
        transaction = self.get_transaction_by_hash(transaction_hash)
        transaction["consensus_data"] = consensus_data

    def set_transaction_appeal(self, transaction_hash: str, appeal: bool):
        transaction = self.get_transaction_by_hash(transaction_hash)
        transaction["appeal"] = appeal

    def set_transaction_timestamp_accepted(
        self, transaction_hash: str, timestamp_accepted: int = None
    ):
        transaction = self.get_transaction_by_hash(transaction_hash)
        if timestamp_accepted:
            transaction["timestamp_accepted"] = timestamp_accepted
        else:
            transaction["timestamp_accepted"] = int(time.time())

    def add_transaction(self, new_transaction: dict):
        self.transactions.append(new_transaction)

    def get_accepted_transactions(self) -> List[dict]:
        result = []
        for transaction in self.transactions:
            if transaction["status"] == TransactionStatus.ACCEPTED.value:
                result.append(transaction)
        return result

    def create_rollup_transaction(self, transaction_hash: str):
        pass

    def set_transaction_appeal_failed(self, transaction_hash: str, appeal_failed: int):
        if appeal_failed < 0:
            raise ValueError("appeal_failed must be a non-negative integer")
        transaction = self.get_transaction_by_hash(transaction_hash)
        transaction["appeal_failed"] = appeal_failed


class SnapshotMock:
    def __init__(self, nodes):
        self.nodes = nodes

    def get_all_validators(self):
        return self.nodes


def transaction_to_dict(transaction: Transaction) -> dict:
    return {
        "hash": transaction.hash,
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
        "leader_only": transaction.leader_only,
        "appeal": transaction.appeal,
        "timestamp_accepted": transaction.timestamp_accepted,
        "appeal_failed": transaction.appeal_failed,
    }


def contract_snapshot_factory(address: str):
    class ContractSnapshotMock:
        def __init__(self):
            self.address = address

        def update_contract_state(self, state: str):
            pass

    return ContractSnapshotMock()


@pytest.mark.asyncio
async def test_exec_transaction(managed_thread):
    """
    Minor smoke checks for the happy path of a transaction execution
    """

    transaction = Transaction(
        hash="transaction_hash",
        from_address="from_address",
        to_address="to_address",
        status=TransactionStatus.PENDING,
        type=TransactionType.RUN_CONTRACT,
    )

    nodes = [
        {
            "address": f"address{i}",
            "stake": i + 1,
            "provider": f"provider{i}",
            "model": f"model{i}",
            "config": f"config{i}",
        }
        for i in range(3)
    ]

    created_nodes = []

    def node_factory(
        node: dict,
        mode: ExecutionMode,
        contract_snapshot: ContractSnapshot,
        receipt: Receipt | None,
        msg_handler: MessageHandler,
        contract_snapshot_factory: Callable[[str], ContractSnapshot],
    ):
        mock = Mock(Node)

        mock.validator_mode = mode
        mock.address = node["address"]
        mock.leader_receipt = receipt

        mock.exec_transaction = AsyncMock(
            return_value=Receipt(
                vote=Vote.AGREE,
                class_name="",
                calldata=b"",
                mode=mode,
                gas_used=0,
                contract_state="",
                node_config={"address": node["address"]},
                eq_outputs={},
                execution_result=ExecutionResultStatus.SUCCESS,
                error=None,
            )
        )

        created_nodes.append(mock)

        return mock

    transactions_processor = TransactionsProcessorMock(
        [transaction_to_dict(transaction)]
    )

    msg_handler_mock = Mock(MessageHandler)

    consensus = ConsensusAlgorithm(None, msg_handler_mock)

    managed_thread(transactions_processor, msg_handler_mock, nodes, node_factory)

    await consensus.exec_transaction(
        transaction=transaction,
        transactions_processor=transactions_processor,
        snapshot=SnapshotMock(nodes),
        accounts_manager=AccountsManagerMock(),
        contract_snapshot_factory=contract_snapshot_factory,
        node_factory=node_factory,
    )

    assert len(created_nodes) == len(nodes)

    for node in created_nodes:
        node.exec_transaction.assert_awaited_once_with(transaction)

    time.sleep(DEFAULT_FINALITY_WINDOW + 2)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.FINALIZED.value
    )

    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": [
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
            TransactionStatus.FINALIZED,
        ]
    }


@pytest.mark.asyncio
async def test_exec_transaction_no_consensus():
    """
    Scenario: all nodes disagree on the transaction execution, leaving the transaction in UNDETERMINED state
    Tests that consensus algorithm correctly rotates the leader when majority of nodes disagree
    """

    transaction = Transaction(
        hash="transaction_hash",
        from_address="from_address",
        to_address="to_address",
        status=TransactionStatus.PENDING,
        type=TransactionType.RUN_CONTRACT,
    )

    nodes = [
        {
            "address": f"address{i}",
            "stake": i + 1,
            "provider": f"provider{i}",
            "model": f"model{i}",
            "config": f"config{i}",
        }
        for i in range(3)
    ]

    created_nodes = []

    def node_factory(
        node: dict,
        mode: ExecutionMode,
        contract_snapshot: ContractSnapshot,
        receipt: Receipt | None,
        msg_handler: MessageHandler,
        contract_snapshot_factory: Callable[[str], ContractSnapshot],
    ):
        mock = Mock(Node)

        mock.validator_mode = mode
        mock.address = node["address"]
        mock.leader_receipt = receipt

        mock.exec_transaction = AsyncMock(
            return_value=Receipt(
                vote=Vote.DISAGREE,
                class_name="",
                calldata=b"",
                mode=mode,
                gas_used=0,
                contract_state="",
                node_config={"address": node["address"]},
                eq_outputs={},
                execution_result=ExecutionResultStatus.SUCCESS,
                error=None,
            )
        )

        created_nodes.append(mock)

        return mock

    transactions_processor = TransactionsProcessorMock(
        [transaction_to_dict(transaction)]
    )

    msg_handler_mock = Mock(MessageHandler)

    await ConsensusAlgorithm(None, msg_handler_mock).exec_transaction(
        transaction=transaction,
        transactions_processor=transactions_processor,
        snapshot=SnapshotMock(nodes),
        accounts_manager=AccountsManagerMock(),
        contract_snapshot_factory=contract_snapshot_factory,
        node_factory=node_factory,
    )

    assert len(created_nodes) == len(nodes) ** 2

    for node in created_nodes:
        node.exec_transaction.assert_awaited_once_with(transaction)

    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": [
            TransactionStatus.PROPOSING,  # leader 1
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.PROPOSING,  # rotation, leader 2
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.PROPOSING,  # rotation, leader 3
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.UNDETERMINED,  # all disagree
        ]
    }


@pytest.mark.asyncio
async def test_exec_transaction_one_disagreement(managed_thread):
    """
    Scenario: first round is disagreement, second round is agreement
    Tests that consensus algorithm correctly rotates the leader when majority of nodes disagree
    """

    transaction = Transaction(
        hash="transaction_hash",
        from_address="from_address",
        to_address="to_address",
        status=TransactionStatus.PENDING,
        type=TransactionType.RUN_CONTRACT,
    )

    nodes = [
        {
            "address": f"address{i}",
            "stake": i + 1,
            "provider": f"provider{i}",
            "model": f"model{i}",
            "config": f"config{i}",
        }
        for i in range(3)
    ]

    created_nodes = []

    def node_factory(
        node: dict,
        mode: ExecutionMode,
        contract_snapshot: ContractSnapshot,
        receipt: Receipt | None,
        msg_handler: MessageHandler,
        contract_snapshot_factory: Callable[[str], ContractSnapshot],
    ):
        mock = Mock(Node)

        mock.validator_mode = mode
        mock.address = node["address"]
        mock.leader_receipt = receipt

        async def exec_transaction(transaction: Transaction):
            return Receipt(
                vote=(
                    Vote.AGREE
                    if ((len(created_nodes) - 1) // len(nodes))
                    == 1  # only agree in the second round
                    else Vote.DISAGREE
                ),
                class_name="",
                calldata=b"",
                mode=mode,
                gas_used=0,
                contract_state="",
                node_config={"address": node["address"]},
                eq_outputs={},
                execution_result=ExecutionResultStatus.SUCCESS,
                error=None,
            )

        mock.exec_transaction.side_effect = exec_transaction

        created_nodes.append(mock)

        return mock

    transactions_processor = TransactionsProcessorMock(
        [transaction_to_dict(transaction)]
    )

    msg_handler_mock = Mock(MessageHandler)

    consensus = ConsensusAlgorithm(None, msg_handler_mock)

    managed_thread(transactions_processor, msg_handler_mock, nodes, node_factory)

    await consensus.exec_transaction(
        transaction=transaction,
        transactions_processor=transactions_processor,
        snapshot=SnapshotMock(nodes),
        accounts_manager=AccountsManagerMock(),
        contract_snapshot_factory=contract_snapshot_factory,
        node_factory=node_factory,
    )

    time.sleep(DEFAULT_FINALITY_WINDOW + 2)

    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": [
            TransactionStatus.PROPOSING,  # leader 1
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.PROPOSING,  # rotation, leader 2
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
            TransactionStatus.FINALIZED,
        ]
    }

    assert len(created_nodes) == len(nodes) * 2

    for node in created_nodes:
        node.exec_transaction.assert_awaited_once_with(transaction)


def test_rotate():
    input = [1, 2, 3, 4, 5]
    iterator = rotate(input)

    assert next(iterator) == [1, 2, 3, 4, 5]
    assert next(iterator) == [2, 3, 4, 5, 1]
    assert next(iterator) == [3, 4, 5, 1, 2]
    assert next(iterator) == [4, 5, 1, 2, 3]
    assert next(iterator) == [5, 1, 2, 3, 4]

    with pytest.raises(StopIteration):
        next(iterator)


async def _appeal_window(
    stop_event: threading.Event,
    transactions_processor: TransactionsProcessorMock,
    msg_handler: MessageHandler,
    nodes: list[dict],
    node_factory: Callable[
        [
            dict,
            ExecutionMode,
            ContractSnapshot,
            Receipt | None,
            MessageHandler,
            Callable[[str], ContractSnapshot],
        ],
        Node,
    ],
):
    while not stop_event.is_set():
        accepted_transactions = transactions_processor.get_accepted_transactions()
        for transaction in accepted_transactions:
            transaction = Transaction.from_dict(transaction)
            if not transaction.appeal:
                if (
                    int(time.time()) - transaction.timestamp_accepted
                ) > DEFAULT_FINALITY_WINDOW:
                    context = TransactionContext(
                        transaction=transaction,
                        transactions_processor=transactions_processor,
                        snapshot=SnapshotMock(nodes),
                        accounts_manager=AccountsManagerMock(),
                        contract_snapshot_factory=contract_snapshot_factory,
                        node_factory=node_factory,
                        msg_handler=msg_handler,
                    )
                    state = FinalizingState()
                    await state.handle(context)

            else:
                chain_snapshot = SnapshotMock(nodes)
                context = TransactionContext(
                    transaction=transaction,
                    transactions_processor=transactions_processor,
                    snapshot=chain_snapshot,
                    accounts_manager=AccountsManagerMock(),
                    contract_snapshot_factory=contract_snapshot_factory,
                    node_factory=node_factory,
                    msg_handler=msg_handler,
                )
                context.consensus_data.leader_receipt = (
                    transaction.consensus_data.leader_receipt
                )
                n = len(transaction.consensus_data.validators) + 1
                current_validators_addresses = {
                    validator.node_config["address"]
                    for validator in transaction.consensus_data.validators
                }
                current_validators_addresses.add(
                    transaction.consensus_data.leader_receipt.node_config["address"]
                )
                try:
                    context.remaining_validators = (
                        ConsensusAlgorithm.get_extra_validators(
                            chain_snapshot, transaction.consensus_data
                        )
                    )
                except ValueError as e:
                    print(e, transaction)
                    context.transactions_processor.set_transaction_appeal(
                        context.transaction.hash, False
                    )
                    context.transaction.appeal = False
                else:
                    context.num_validators = len(context.remaining_validators)
                    assert context.num_validators == n + 2

                    context.votes = {}
                    context.contract_snapshot = context.contract_snapshot_factory(
                        transaction.to_address
                    )

                    new_validators_addresses = {
                        validator["address"]
                        for validator in context.remaining_validators
                    }
                    assert new_validators_addresses != current_validators_addresses

                    # State transitions
                    state = CommittingState()
                    while True:
                        next_state = await state.handle(context)
                        if next_state is None:
                            break
                        assert len(context.validator_nodes) == n + 2
                        state = next_state

        await asyncio.sleep(1)


def run_async_task_in_thread(
    stop_event: threading.Event,
    transactions_processor: TransactionsProcessorMock,
    msg_handler: MessageHandler,
    nodes: list[dict],
    node_factory: Callable[
        [
            dict,
            ExecutionMode,
            ContractSnapshot,
            Receipt | None,
            MessageHandler,
            Callable[[str], ContractSnapshot],
        ],
        Node,
    ],
):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(
            _appeal_window(
                stop_event, transactions_processor, msg_handler, nodes, node_factory
            )
        )
    finally:
        loop.close()


@pytest.fixture
def managed_thread(request):
    def start_thread(
        transactions_processor: TransactionsProcessorMock,
        msg_handler: MessageHandler,
        nodes: list[dict],
        node_factory: Callable[
            [
                dict,
                ExecutionMode,
                ContractSnapshot,
                Receipt | None,
                MessageHandler,
                Callable[[str], ContractSnapshot],
            ],
            Node,
        ],
    ):
        stop_event = threading.Event()
        thread = threading.Thread(
            target=run_async_task_in_thread,
            args=(stop_event, transactions_processor, msg_handler, nodes, node_factory),
        )
        thread.start()

        def fin():
            stop_event.set()
            thread.join()

        request.addfinalizer(fin)

        return thread

    return start_thread


@pytest.mark.asyncio
async def test_exec_accepted_appeal_fail(managed_thread):
    """
    Test that a transaction can be appealed after being accepted where the appeal fails. This verifies that:
    1. The transaction can enter appeal state
    2. New validators are selected to process the appeal
    3. The appeal is processed but fails
    4. The transaction goes back to the active state
    5. The appeal window is not reset
    6. The transaction is finalized after the appeal window
    The states the transaction goes through are:
        PROPOSING -> COMMITTING -> REVEALING -> ACCEPTED -appeal-> COMMITTING -> REVEALING -appeal-fail-> ACCEPTED -no-appeal-> FINALIZED
    """
    transaction = Transaction(
        hash="transaction_hash",
        from_address="from_address",
        to_address="to_address",
        status=TransactionStatus.PENDING,
        type=TransactionType.RUN_CONTRACT,
    )

    nodes = [
        {
            "address": f"address{i}",
            "stake": i + 1,
            "provider": f"provider{i}",
            "model": f"model{i}",
            "config": f"config{i}",
        }
        for i in range(2 * DEFAULT_VALIDATORS_COUNT + 2)
    ]

    created_nodes = []

    def node_factory(
        node: dict,
        mode: ExecutionMode,
        contract_snapshot: ContractSnapshot,
        receipt: Receipt | None,
        msg_handler: MessageHandler,
        contract_snapshot_factory: Callable[[str], ContractSnapshot],
    ):
        mock = Mock(Node)

        mock.validator_mode = mode
        mock.address = node["address"]
        mock.leader_receipt = receipt

        mock.exec_transaction = AsyncMock(
            return_value=Receipt(
                vote=Vote.AGREE,
                class_name="",
                calldata=b"",
                mode=mode,
                gas_used=0,
                contract_state="",
                node_config={"address": node["address"]},
                eq_outputs={},
                execution_result=ExecutionResultStatus.SUCCESS,
                error=None,
            )
        )

        created_nodes.append(mock)

        return mock

    transactions_processor = TransactionsProcessorMock(
        [transaction_to_dict(transaction)]
    )

    msg_handler_mock = Mock(MessageHandler)

    managed_thread(transactions_processor, msg_handler_mock, nodes, node_factory)

    await ConsensusAlgorithm(None, msg_handler_mock).exec_transaction(
        transaction=transaction,
        transactions_processor=transactions_processor,
        snapshot=SnapshotMock(nodes),
        accounts_manager=AccountsManagerMock(),
        contract_snapshot_factory=contract_snapshot_factory,
        node_factory=node_factory,
    )

    assert len(created_nodes) == DEFAULT_VALIDATORS_COUNT

    for node in created_nodes:
        node.exec_transaction.assert_awaited_once_with(transaction)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.ACCEPTED.value
    )
    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == False
    )

    timestamp_accepted_1 = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["timestamp_accepted"]

    transactions_processor.set_transaction_appeal(transaction.hash, True)
    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == True
    )

    time.sleep(DEFAULT_FINALITY_WINDOW + 2)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.FINALIZED.value
    )

    assert (
        len(
            transactions_processor.get_transaction_by_hash(transaction.hash)[
                "consensus_data"
            ]["validators"]
        )
        == 2 * DEFAULT_VALIDATORS_COUNT + 1
    )

    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": [
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
            TransactionStatus.FINALIZED,
        ]
    }
    assert len(created_nodes) == 2 * DEFAULT_VALIDATORS_COUNT + 2

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)[
            "timestamp_accepted"
        ]
        == timestamp_accepted_1
    )


@pytest.mark.asyncio
async def test_exec_accepted_appeal_no_extra_validators(managed_thread):
    """
    Test that a transaction goes to finalized state when there are no extra validators to process the appeal. This verifies that:
    1. The transaction can enter appeal state
    2. New validators are selected to process the appeal but there are no extra validators anymore
    3. The appeal is not processed and fails
    4. The transaction stays in the active state and appeal window is not reset
    5. The transaction is finalized after the appeal window
    The states the transaction goes through are:
        PROPOSING -> COMMITTING -> REVEALING -> ACCEPTED -appeal-> -appeal-fail-> -no-new-appeal-> FINALIZED
    """
    transaction = Transaction(
        hash="transaction_hash",
        from_address="from_address",
        to_address="to_address",
        status=TransactionStatus.PENDING,
        type=TransactionType.RUN_CONTRACT,
    )

    nodes = [
        {
            "address": f"address{i}",
            "stake": i + 1,
            "provider": f"provider{i}",
            "model": f"model{i}",
            "config": f"config{i}",
        }
        for i in range(DEFAULT_VALIDATORS_COUNT)
    ]

    created_nodes = []

    def node_factory(
        node: dict,
        mode: ExecutionMode,
        contract_snapshot: ContractSnapshot,
        receipt: Receipt | None,
        msg_handler: MessageHandler,
        contract_snapshot_factory: Callable[[str], ContractSnapshot],
    ):
        mock = Mock(Node)

        mock.validator_mode = mode
        mock.address = node["address"]
        mock.leader_receipt = receipt

        mock.exec_transaction = AsyncMock(
            return_value=Receipt(
                vote=Vote.AGREE,
                class_name="",
                calldata=b"",
                mode=mode,
                gas_used=0,
                contract_state="",
                node_config={"address": node["address"]},
                eq_outputs={},
                execution_result=ExecutionResultStatus.SUCCESS,
                error=None,
            )
        )

        created_nodes.append(mock)

        return mock

    transactions_processor = TransactionsProcessorMock(
        [transaction_to_dict(transaction)]
    )

    msg_handler_mock = Mock(MessageHandler)

    managed_thread(transactions_processor, msg_handler_mock, nodes, node_factory)

    await ConsensusAlgorithm(None, msg_handler_mock).exec_transaction(
        transaction=transaction,
        transactions_processor=transactions_processor,
        snapshot=SnapshotMock(nodes),
        accounts_manager=AccountsManagerMock(),
        contract_snapshot_factory=contract_snapshot_factory,
        node_factory=node_factory,
    )

    assert len(created_nodes) == DEFAULT_VALIDATORS_COUNT

    for node in created_nodes:
        node.exec_transaction.assert_awaited_once_with(transaction)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.ACCEPTED.value
    )
    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == False
    )

    timestamp_accepted_1 = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["timestamp_accepted"]

    transactions_processor.set_transaction_appeal(transaction.hash, True)
    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == True
    )

    time.sleep(DEFAULT_FINALITY_WINDOW + 2)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.FINALIZED.value
    )

    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": [
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
            TransactionStatus.FINALIZED,
        ]
    }

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)[
            "timestamp_accepted"
        ]
        == timestamp_accepted_1
    )


@pytest.mark.asyncio
async def test_exec_accepted_appeal_successful(managed_thread):
    """
    Test that a transaction can be appealed successfully after being accepted. This verifies that:
    1. The transaction can enter appeal state
    2. New validators are selected to process the appeal
    3. The appeal is processed successfully
    4. The transaction goes back to the pending state
    5. The consensus algorithm removed the old leader
    6. The consensus algorithm goes through committing and revealing states with an increased number of validators
    7. The transaction is in the accepted state with an updated appeal window
    8. The transaction is finalized after the appeal window
    The states the transaction goes through are:
        PROPOSING -> COMMITTING -> REVEALING -> ACCEPTED -appeal-> COMMITTING -> REVEALING -appeal-success->
        PENDING -> PROPOSING -> COMMITTING -> REVEALING -> ACCEPTED -no-appeal-> FINALIZED
    """
    transaction = Transaction(
        hash="transaction_hash",
        from_address="from_address",
        to_address="to_address",
        status=TransactionStatus.PENDING,
        type=TransactionType.RUN_CONTRACT,
    )

    nodes = [
        {
            "address": f"address{i}",
            "stake": i + 1,
            "provider": f"provider{i}",
            "model": f"model{i}",
            "config": f"config{i}",
        }
        for i in range(2 * DEFAULT_VALIDATORS_COUNT + 2)
    ]

    created_nodes = []

    def node_factory(
        node: dict,
        mode: ExecutionMode,
        contract_snapshot: ContractSnapshot,
        receipt: Receipt | None,
        msg_handler: MessageHandler,
        contract_snapshot_factory: Callable[[str], ContractSnapshot],
    ):
        mock = Mock(Node)

        mock.validator_mode = mode
        mock.address = node["address"]
        mock.leader_receipt = receipt

        def get_vote():
            """ "
            Leader agrees + 4 validators agree.
            Appeal: 4 validators disagree + 3 validators agree. So appeal succeeds.
            """
            if len(created_nodes) < 5:
                vote = Vote.AGREE
            elif (len(created_nodes) >= 5) and (len(created_nodes) < 5 + 4):
                vote = Vote.DISAGREE
            else:
                vote = Vote.AGREE

            return vote

        mock.exec_transaction = AsyncMock(
            return_value=Receipt(
                vote=get_vote(),
                class_name="",
                calldata=b"",
                mode=mode,
                gas_used=0,
                contract_state="",
                node_config={"address": node["address"]},
                eq_outputs={},
                execution_result=ExecutionResultStatus.SUCCESS,
                error=None,
            )
        )

        created_nodes.append(mock)

        return mock

    transactions_processor = TransactionsProcessorMock(
        [transaction_to_dict(transaction)]
    )

    msg_handler_mock = Mock(MessageHandler)

    managed_thread(transactions_processor, msg_handler_mock, nodes, node_factory)

    await ConsensusAlgorithm(None, msg_handler_mock).exec_transaction(
        transaction=transaction,
        transactions_processor=transactions_processor,
        snapshot=SnapshotMock(nodes),
        accounts_manager=AccountsManagerMock(),
        contract_snapshot_factory=contract_snapshot_factory,
        node_factory=node_factory,
    )

    expected_nb_created_nodes = DEFAULT_VALIDATORS_COUNT
    assert len(created_nodes) == expected_nb_created_nodes

    for node in created_nodes:
        node.exec_transaction.assert_awaited_once_with(transaction)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.ACCEPTED.value
    )
    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == False
    )

    timestamp_accepted_1 = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["timestamp_accepted"]

    transactions_processor.set_transaction_appeal(transaction.hash, True)
    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == True
    )

    time.sleep(DEFAULT_FINALITY_WINDOW + 2)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.PENDING.value
    )

    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": [
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.PENDING,
        ]
    }

    expected_nb_created_nodes += expected_nb_created_nodes + 2
    assert len(created_nodes) == expected_nb_created_nodes

    transaction_dict = transactions_processor.get_transaction_by_hash(transaction.hash)
    validator_set_addresses = {
        validator["node_config"]["address"]
        for validator in transaction_dict["consensus_data"]["validators"]
    }
    old_leader_address = transaction_dict["consensus_data"]["leader_receipt"][
        "node_config"
    ]["address"]

    transaction = Transaction.from_dict(
        transaction_dict
    )  # update the variable with the consensus data

    await ConsensusAlgorithm(None, msg_handler_mock).exec_transaction(
        transaction=transaction,
        transactions_processor=transactions_processor,
        snapshot=SnapshotMock(nodes),
        accounts_manager=AccountsManagerMock(),
        contract_snapshot_factory=contract_snapshot_factory,
        node_factory=node_factory,
    )

    time.sleep(DEFAULT_FINALITY_WINDOW + 2)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.FINALIZED.value
    )

    expected_nb_created_nodes += expected_nb_created_nodes - 1
    assert len(created_nodes) == expected_nb_created_nodes

    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": [
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.PENDING,
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
            TransactionStatus.FINALIZED,
        ]
    }

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)[
            "timestamp_accepted"
        ]
        > timestamp_accepted_1
    )

    assert (
        len(
            transactions_processor.get_transaction_by_hash(transaction.hash)[
                "consensus_data"
            ]["validators"]
        )
        == 2 * DEFAULT_VALIDATORS_COUNT
    )

    new_leader_address = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["consensus_data"]["leader_receipt"]["node_config"]["address"]

    assert new_leader_address != old_leader_address
    assert new_leader_address in validator_set_addresses


@pytest.mark.asyncio
async def test_exec_accepted_appeal_successful_rotations_undetermined(managed_thread):
    """
    Test that a transaction can do the rotations when going back to pending after being successful in its appeal. This verifies that:
    1. The transaction can enter appeal state
    2. New validators are selected to process the appeal
    3. The appeal is processed successfully and the transaction goes back to the pending state
    4. Perform all rotation until transaction is undetermined
    The states the transaction goes through are:
        PROPOSING -> COMMITTING -> REVEALING -> ACCEPTED -appeal-> COMMITTING -> REVEALING -appeal-success->
        PENDING -> (PROPOSING -> COMMITTING -> REVEALING) * 11 -> UNDERTERMINED
    """
    transaction = Transaction(
        hash="transaction_hash",
        from_address="from_address",
        to_address="to_address",
        status=TransactionStatus.PENDING,
        type=TransactionType.RUN_CONTRACT,
    )

    nodes = [
        {
            "address": f"address{i}",
            "stake": i + 1,
            "provider": f"provider{i}",
            "model": f"model{i}",
            "config": f"config{i}",
        }
        for i in range(2 * DEFAULT_VALIDATORS_COUNT + 2)
    ]

    created_nodes = []

    def node_factory(
        node: dict,
        mode: ExecutionMode,
        contract_snapshot: ContractSnapshot,
        receipt: Receipt | None,
        msg_handler: MessageHandler,
        contract_snapshot_factory: Callable[[str], ContractSnapshot],
    ):
        mock = Mock(Node)

        mock.validator_mode = mode
        mock.address = node["address"]
        mock.leader_receipt = receipt

        def get_vote():
            """ "
            Leader agrees + 4 validators agree.
            Appeal: 7 validators disagree. So appeal succeeds.
            Rotations: 11 validator disagree.
            """
            if len(created_nodes) < 5:
                vote = Vote.AGREE
            else:
                vote = Vote.DISAGREE

            return vote

        mock.exec_transaction = AsyncMock(
            return_value=Receipt(
                vote=get_vote(),
                class_name="",
                calldata=b"",
                mode=mode,
                gas_used=0,
                contract_state="",
                node_config={"address": node["address"]},
                eq_outputs={},
                execution_result=ExecutionResultStatus.SUCCESS,
                error=None,
            )
        )

        created_nodes.append(mock)

        return mock

    transactions_processor = TransactionsProcessorMock(
        [transaction_to_dict(transaction)]
    )

    msg_handler_mock = Mock(MessageHandler)

    managed_thread(transactions_processor, msg_handler_mock, nodes, node_factory)

    await ConsensusAlgorithm(None, msg_handler_mock).exec_transaction(
        transaction=transaction,
        transactions_processor=transactions_processor,
        snapshot=SnapshotMock(nodes),
        accounts_manager=AccountsManagerMock(),
        contract_snapshot_factory=contract_snapshot_factory,
        node_factory=node_factory,
    )

    expected_nb_created_nodes = DEFAULT_VALIDATORS_COUNT
    assert len(created_nodes) == expected_nb_created_nodes

    for node in created_nodes:
        node.exec_transaction.assert_awaited_once_with(transaction)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.ACCEPTED.value
    )
    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == False
    )

    transactions_processor.set_transaction_appeal(transaction.hash, True)
    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == True
    )

    time.sleep(DEFAULT_FINALITY_WINDOW + 2)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.PENDING.value
    )

    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": [
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.PENDING,
        ]
    }

    expected_nb_created_nodes += expected_nb_created_nodes + 2
    assert len(created_nodes) == expected_nb_created_nodes

    transaction = Transaction.from_dict(
        transactions_processor.get_transaction_by_hash(transaction.hash)
    )  # update the variable with the consensus data

    await ConsensusAlgorithm(None, msg_handler_mock).exec_transaction(
        transaction=transaction,
        transactions_processor=transactions_processor,
        snapshot=SnapshotMock(nodes),
        accounts_manager=AccountsManagerMock(),
        contract_snapshot_factory=contract_snapshot_factory,
        node_factory=node_factory,
    )

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.UNDETERMINED.value
    )

    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": [
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.PENDING,
            *(
                [
                    TransactionStatus.PROPOSING,
                    TransactionStatus.COMMITTING,
                    TransactionStatus.REVEALING,
                ]
                * 11
            ),
            TransactionStatus.UNDETERMINED,
        ]
    }

    assert (
        len(
            transactions_processor.get_transaction_by_hash(transaction.hash)[
                "consensus_data"
            ]["validators"]
        )
        == 2 * DEFAULT_VALIDATORS_COUNT
    )


@pytest.mark.asyncio
async def test_exec_accepted_appeal_successful_twice(managed_thread):
    """
    Test that a transaction can be appealed successfully twice after being accepted. This verifies that:
    1. The transaction can enter appeal state
    2. New validators are selected to process the appeal
    3. The appeal is processed successfully
    4. The transaction goes back to the pending state
    5. The consensus algorithm removed the old leader
    6. The consensus algorithm goes through committing and revealing states with an increased number of validators
    7. The transaction is in the accepted state with an updated appeal window
    8. Do 1-7 again
    9. The transaction is finalized after the appeal window
    The states the transaction goes through are:
        PROPOSING -> COMMITTING -> REVEALING -> ACCEPTED -appeal-> COMMITTING -> REVEALING -appeal-success->
        PENDING -> PROPOSING -> COMMITTING -> REVEALING -> ACCEPTED -appeal-> COMMITTING -> REVEALING -appeal-success->
        PENDING -> PROPOSING -> COMMITTING -> REVEALING -> ACCEPTED -no-appeal-> FINALIZED
    """
    transaction = Transaction(
        hash="transaction_hash",
        from_address="from_address",
        to_address="to_address",
        status=TransactionStatus.PENDING,
        type=TransactionType.RUN_CONTRACT,
    )

    nodes = [
        {
            "address": f"address{i}",
            "stake": i + 1,
            "provider": f"provider{i}",
            "model": f"model{i}",
            "config": f"config{i}",
        }
        for i in range(2 * (2 * DEFAULT_VALIDATORS_COUNT + 1) + 1 + 2)
    ]

    created_nodes = []

    def node_factory(
        node: dict,
        mode: ExecutionMode,
        contract_snapshot: ContractSnapshot,
        receipt: Receipt | None,
        msg_handler: MessageHandler,
        contract_snapshot_factory: Callable[[str], ContractSnapshot],
    ):
        mock = Mock(Node)

        mock.validator_mode = mode
        mock.address = node["address"]
        mock.leader_receipt = receipt

        def get_vote():
            """ "
            Normal: Leader agrees + 4 validators agree.
            Appeal: 7 validators disagree. So appeal succeeds.
            Normal: Leader agrees + 10 validators agree.
            Appeal: 13 validators disagree. So appeal succeeds.
            Normal: Leader agrees + 22 validators agree.
            """
            if len(created_nodes) < 5:
                vote = Vote.AGREE
            elif (len(created_nodes) >= 5) and (len(created_nodes) < 5 + 7):
                vote = Vote.DISAGREE
            elif (len(created_nodes) >= 5 + 7) and (len(created_nodes) < 5 + 7 + 11):
                vote = Vote.AGREE
            elif (len(created_nodes) >= 5 + 7 + 11) and (
                len(created_nodes) < 5 + 7 + 11 + 13
            ):
                vote = Vote.DISAGREE
            else:
                vote = Vote.AGREE

            return vote

        mock.exec_transaction = AsyncMock(
            return_value=Receipt(
                vote=get_vote(),
                class_name="",
                calldata=b"",
                mode=mode,
                gas_used=0,
                contract_state="",
                node_config={"address": node["address"]},
                eq_outputs={},
                execution_result=ExecutionResultStatus.SUCCESS,
                error=None,
            )
        )

        created_nodes.append(mock)

        return mock

    transactions_processor = TransactionsProcessorMock(
        [transaction_to_dict(transaction)]
    )

    msg_handler_mock = Mock(MessageHandler)

    managed_thread(transactions_processor, msg_handler_mock, nodes, node_factory)

    await ConsensusAlgorithm(None, msg_handler_mock).exec_transaction(
        transaction=transaction,
        transactions_processor=transactions_processor,
        snapshot=SnapshotMock(nodes),
        accounts_manager=AccountsManagerMock(),
        contract_snapshot_factory=contract_snapshot_factory,
        node_factory=node_factory,
    )

    expected_nb_created_nodes = DEFAULT_VALIDATORS_COUNT  # 5
    assert len(created_nodes) == expected_nb_created_nodes

    for node in created_nodes:
        node.exec_transaction.assert_awaited_once_with(transaction)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.ACCEPTED.value
    )

    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": [
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
        ]
    }

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == False
    )

    timestamp_accepted_1 = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["timestamp_accepted"]

    transactions_processor.set_transaction_appeal(transaction.hash, True)
    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == True
    )

    time.sleep(DEFAULT_FINALITY_WINDOW + 2)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.PENDING.value
    )

    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": [
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.PENDING,
        ]
    }

    expected_nb_created_nodes += DEFAULT_VALIDATORS_COUNT + 2  # 5 + 7 = 12
    assert len(created_nodes) == expected_nb_created_nodes

    transaction_dict = transactions_processor.get_transaction_by_hash(transaction.hash)
    validator_set_addresses = {
        validator["node_config"]["address"]
        for validator in transaction_dict["consensus_data"]["validators"]
    }
    old_leader_address = transaction_dict["consensus_data"]["leader_receipt"][
        "node_config"
    ]["address"]

    transaction = Transaction.from_dict(
        transaction_dict
    )  # update the variable with the consensus data

    await ConsensusAlgorithm(None, msg_handler_mock).exec_transaction(
        transaction=transaction,
        transactions_processor=transactions_processor,
        snapshot=SnapshotMock(nodes),
        accounts_manager=AccountsManagerMock(),
        contract_snapshot_factory=contract_snapshot_factory,
        node_factory=node_factory,
    )

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.ACCEPTED.value
    )

    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": [
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.PENDING,
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
        ]
    }

    expected_nb_created_nodes += 2 * DEFAULT_VALIDATORS_COUNT + 1  # 12 + 11 = 23
    assert len(created_nodes) == expected_nb_created_nodes

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == False
    )

    timestamp_accepted_2 = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["timestamp_accepted"]
    assert timestamp_accepted_2 > timestamp_accepted_1

    assert (
        len(
            transactions_processor.get_transaction_by_hash(transaction.hash)[
                "consensus_data"
            ]["validators"]
        )
        == 2 * DEFAULT_VALIDATORS_COUNT
    )

    new_leader_address = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["consensus_data"]["leader_receipt"]["node_config"]["address"]

    assert new_leader_address != old_leader_address
    assert new_leader_address in validator_set_addresses

    transactions_processor.set_transaction_appeal(transaction.hash, True)
    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == True
    )

    time.sleep(DEFAULT_FINALITY_WINDOW + 2)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.PENDING.value
    )

    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": [
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.PENDING,
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.PENDING,
        ]
    }

    expected_nb_created_nodes += (2 * DEFAULT_VALIDATORS_COUNT + 1) + 2  # 23 + 13 = 36
    assert len(created_nodes) == expected_nb_created_nodes

    transaction_dict = transactions_processor.get_transaction_by_hash(transaction.hash)
    validator_set_addresses = {
        validator["node_config"]["address"]
        for validator in transaction_dict["consensus_data"]["validators"]
    }
    old_leader_address = transaction_dict["consensus_data"]["leader_receipt"][
        "node_config"
    ]["address"]

    transaction = Transaction.from_dict(
        transaction_dict
    )  # update the variable with the consensus data

    await ConsensusAlgorithm(None, msg_handler_mock).exec_transaction(
        transaction=transaction,
        transactions_processor=transactions_processor,
        snapshot=SnapshotMock(nodes),
        accounts_manager=AccountsManagerMock(),
        contract_snapshot_factory=contract_snapshot_factory,
        node_factory=node_factory,
    )

    time.sleep(DEFAULT_FINALITY_WINDOW + 2)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.FINALIZED.value
    )

    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": [
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
            *(
                [
                    TransactionStatus.COMMITTING,
                    TransactionStatus.REVEALING,
                    TransactionStatus.PENDING,
                    TransactionStatus.PROPOSING,
                    TransactionStatus.COMMITTING,
                    TransactionStatus.REVEALING,
                    TransactionStatus.ACCEPTED,
                ]
                * 2
            ),
            TransactionStatus.FINALIZED,
        ]
    }

    expected_nb_created_nodes += (
        2 * (2 * DEFAULT_VALIDATORS_COUNT + 1) + 2
    ) - 1  # 36 + 23 = 58
    assert len(created_nodes) == expected_nb_created_nodes

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)[
            "timestamp_accepted"
        ]
        > timestamp_accepted_2
    )

    assert len(
        transactions_processor.get_transaction_by_hash(transaction.hash)[
            "consensus_data"
        ]["validators"]
    ) == 2 * (2 * DEFAULT_VALIDATORS_COUNT + 1)

    new_leader_address = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["consensus_data"]["leader_receipt"]["node_config"]["address"]

    assert new_leader_address != old_leader_address
    assert new_leader_address in validator_set_addresses
