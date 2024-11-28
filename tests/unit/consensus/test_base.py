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

DEFAULT_FINALITY_WINDOW = 5  # seconds


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

    def set_transaction_timestamp_awaiting_finalization(
        self, transaction_hash: str, timestamp_awaiting_finalization: int = None
    ):
        transaction = self.get_transaction_by_hash(transaction_hash)
        if timestamp_awaiting_finalization:
            transaction["timestamp_awaiting_finalization"] = (
                timestamp_awaiting_finalization
            )
        else:
            transaction["timestamp_awaiting_finalization"] = int(time.time())

    def add_transaction(self, new_transaction: dict):
        self.transactions.append(new_transaction)

    def get_accepted_undetermined_transactions(self) -> List[dict]:
        result = []
        for transaction in self.transactions:
            if (transaction["status"] == TransactionStatus.ACCEPTED.value) or (
                transaction["status"] == TransactionStatus.UNDETERMINED.value
            ):
                result.append(transaction)
        return sorted(result, key=lambda x: x["timestamp_awaiting_finalization"])

    def create_rollup_transaction(self, transaction_hash: str):
        pass

    def set_transaction_appeal_failed(self, transaction_hash: str, appeal_failed: int):
        if appeal_failed < 0:
            raise ValueError("appeal_failed must be a non-negative integer")
        transaction = self.get_transaction_by_hash(transaction_hash)
        transaction["appeal_failed"] = appeal_failed

    def set_transaction_appeal_undetermined(
        self, transaction_hash: str, appeal_undetermined: bool
    ):
        transaction = self.get_transaction_by_hash(transaction_hash)
        transaction["appeal_undetermined"] = appeal_undetermined


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
        "timestamp_awaiting_finalization": transaction.timestamp_awaiting_finalization,
        "appeal_failed": transaction.appeal_failed,
        "appeal_undetermined": transaction.appeal_undetermined,
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

    managed_thread(transactions_processor, msg_handler_mock, nodes, node_factory)

    await ConsensusAlgorithm(None, msg_handler_mock).exec_transaction(
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
async def test_exec_transaction_no_consensus(managed_thread):
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

    managed_thread(transactions_processor, msg_handler_mock, nodes, node_factory)

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

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.UNDETERMINED.value
    )

    time.sleep(DEFAULT_FINALITY_WINDOW + 2)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.FINALIZED.value
    )

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
            TransactionStatus.FINALIZED,
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

    managed_thread(transactions_processor, msg_handler_mock, nodes, node_factory)

    await ConsensusAlgorithm(None, msg_handler_mock).exec_transaction(
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
        accepted_undetermined_transactions = (
            transactions_processor.get_accepted_undetermined_transactions()
        )
        for transaction in accepted_undetermined_transactions:
            transaction = Transaction.from_dict(transaction)
            if not transaction.appeal:
                if (
                    int(time.time()) - transaction.timestamp_awaiting_finalization
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
                # Handle transactions that are appealed
                if transaction.status == TransactionStatus.UNDETERMINED:
                    # Leader appeal
                    # Appeal data member is used in the frontend for both types of appeals
                    # Here the type is refined based on the status
                    transactions_processor.set_transaction_appeal_undetermined(
                        transaction.hash, True
                    )
                    transactions_processor.set_transaction_appeal(
                        transaction.hash, False
                    )

                    # Set the status to PENDING, transaction will be picked up by _crawl_snapshot
                    ConsensusAlgorithm.dispatch_transaction_status_update(
                        transactions_processor,
                        transaction.hash,
                        TransactionStatus.PENDING,
                        msg_handler,
                    )
                    # Create a rollup transaction
                    transactions_processor.create_rollup_transaction(transaction.hash)

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
                    nb_current_validators = (
                        len(transaction.consensus_data.validators) + 1
                    )
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
                                chain_snapshot,
                                transaction.consensus_data,
                                transaction.appeal_failed,
                            )
                        )
                    except ValueError as e:
                        print(e, transaction)
                        context.transactions_processor.set_transaction_appeal(
                            context.transaction.hash, False
                        )
                        context.transaction.appeal = False
                    else:
                        if transaction.appeal_failed == 0:
                            n = nb_current_validators
                            nb_validators_processing_appeal = n + 2
                        elif transaction.appeal_failed == 1:
                            n = (nb_current_validators - 2) // 2
                            nb_validators_processing_appeal = 2 * n + 3
                        else:
                            n = (nb_current_validators - 3) // (
                                2 * transaction.appeal_failed - 1
                            )
                            nb_validators_processing_appeal = 4 * n + 3

                        context.num_validators = len(context.remaining_validators)
                        assert context.num_validators == nb_validators_processing_appeal

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
                            assert (
                                len(context.validator_nodes)
                                == nb_validators_processing_appeal
                            )
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

    timestamp_awaiting_finalization_1 = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["timestamp_awaiting_finalization"]

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
            "timestamp_awaiting_finalization"
        ]
        == timestamp_awaiting_finalization_1
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

    timestamp_awaiting_finalization_1 = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["timestamp_awaiting_finalization"]

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
            "timestamp_awaiting_finalization"
        ]
        == timestamp_awaiting_finalization_1
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

    timestamp_awaiting_finalization_1 = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["timestamp_awaiting_finalization"]

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
            "timestamp_awaiting_finalization"
        ]
        > timestamp_awaiting_finalization_1
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

    timestamp_awaiting_finalization_1 = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["timestamp_awaiting_finalization"]

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

    timestamp_awaiting_finalization_2 = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["timestamp_awaiting_finalization"]
    assert timestamp_awaiting_finalization_2 > timestamp_awaiting_finalization_1

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
            "timestamp_awaiting_finalization"
        ]
        > timestamp_awaiting_finalization_2
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


@pytest.mark.asyncio
async def test_exec_accepted_appeal_fail_three_times(managed_thread):
    """
    Test that a transaction can be appealed after being accepted where the appeal fails three times. This verifies that:
    1. The transaction can enter appeal state after being accepted
    2. New validators are selected to process the appeal:
        2.1 N+2 new validators where appeal_failed = 0
        2.2 N+2 old validators from 2.1 + N+1 new validators = 2N+3 validators where appeal_failed = 1
        2.3 2N+3 old validators from 2.2 + 2N new validators = 4N+3 validators where appeal_failed = 2
        2.4 No need to continue testing more validators as it follows the same pattern as 2.3 calculation
    3. The appeal is processed but fails
    4. The transaction goes back to the active state
    5. The appeal window is not reset
    6. Redo 1-5 two more times to check if the correct amount of validators are selected. First time takes 2.2 validators, second time takes 2.3 validators.
    7. The transaction is finalized after the appeal window
    The states the transaction goes through are:
        PROPOSING -> COMMITTING -> REVEALING -> ACCEPTED (-appeal-> COMMITTING -> REVEALING -appeal-fail-> ACCEPTED)x3 -no-appeal-> FINALIZED
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
        for i in range(5 * DEFAULT_VALIDATORS_COUNT + 3)
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

    for node in created_nodes:
        node.exec_transaction.assert_awaited_once_with(transaction)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.ACCEPTED.value
    )

    timestamp_awaiting_finalization_1 = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["timestamp_awaiting_finalization"]

    n = DEFAULT_VALIDATORS_COUNT
    nb_validators_processing_appeal = n
    nb_created_nodes = n

    assert (
        len(
            transactions_processor.get_transaction_by_hash(transaction.hash)[
                "consensus_data"
            ]["validators"]
        )
        == nb_validators_processing_appeal - 1
    )

    assert len(created_nodes) == nb_created_nodes

    validator_set_addresses = {
        validator["node_config"]["address"]
        for validator in transactions_processor.get_transaction_by_hash(
            transaction.hash
        )["consensus_data"]["validators"]
    }

    leader_address = transactions_processor.get_transaction_by_hash(transaction.hash)[
        "consensus_data"
    ]["leader_receipt"]["node_config"]["address"]

    for appeal_failed in range(3):
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

        time.sleep(1.5)

        assert (
            transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
            == TransactionStatus.ACCEPTED.value
        )

        assert (
            transactions_processor.get_transaction_by_hash(transaction.hash)[
                "timestamp_awaiting_finalization"
            ]
            == timestamp_awaiting_finalization_1
        )

        if appeal_failed == 0:
            nb_validators_processing_appeal += n + 2
        elif appeal_failed == 1:
            nb_validators_processing_appeal += n + 1
        else:
            nb_validators_processing_appeal += 2 * n  # 5, 12, 18, 28

        nb_created_nodes += (
            nb_validators_processing_appeal - n
        )  # 5, 7, 13, 23 -> 5, 12, 25, 48

        assert (
            transactions_processor.get_transaction_by_hash(transaction.hash)[
                "appeal_failed"
            ]
            == appeal_failed + 1
        )

        assert (
            len(
                transactions_processor.get_transaction_by_hash(transaction.hash)[
                    "consensus_data"
                ]["validators"]
            )
            == nb_validators_processing_appeal
            - 1  # minus one because there is no leader receipt in the validator receipts list
        )

        assert len(created_nodes) == nb_created_nodes

        validator_set_addresses_old = validator_set_addresses
        validator_set_addresses = {
            validator["node_config"]["address"]
            for validator in transactions_processor.get_transaction_by_hash(
                transaction.hash
            )["consensus_data"]["validators"]
        }

        assert validator_set_addresses_old != validator_set_addresses
        assert validator_set_addresses_old.issubset(validator_set_addresses)

        assert (
            leader_address
            == transactions_processor.get_transaction_by_hash(transaction.hash)[
                "consensus_data"
            ]["leader_receipt"]["node_config"]["address"]
        )
        assert leader_address not in validator_set_addresses

    time.sleep(DEFAULT_FINALITY_WINDOW + 2)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.FINALIZED.value
    )

    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": [
            TransactionStatus.PROPOSING,
            *(
                [
                    TransactionStatus.COMMITTING,
                    TransactionStatus.REVEALING,
                    TransactionStatus.ACCEPTED,
                ]
                * 4
            ),
            TransactionStatus.FINALIZED,
        ]
    }


@pytest.mark.asyncio
async def test_exec_accepted_appeal_successful_fail_successful(managed_thread):
    """
    Test that a transaction can be appealed successfully, then appeal fails, then be successfully appealed again after being accepted. This verifies that:
    1. The transaction can enter appeal state
    2. New validators are selected to process the appeal
    3. The appeal is processed successfully
    4. The transaction goes back to the pending state
    5. The consensus algorithm removes the old leader
    6. The consensus algorithm goes through committing and revealing states with an increased number of validators
    7. The transaction is in the accepted state with an updated appeal window
    8. The transaction can enter appeal state
    9. New validators are selected to process the appeal
    10. The appeal is processed but fails
    11. The transaction goes back to the active state
    12. The appeal window is not reset
    13. Redo 1-7
    14. The transaction is finalized after the appeal window
    The states the transaction goes through are:
        PROPOSING -> COMMITTING -> REVEALING -> ACCEPTED
        -appeal-> COMMITTING -> REVEALING -appeal-success->
        PENDING -> PROPOSING -> COMMITTING -> REVEALING -> ACCEPTED ->
        -appeal-> COMMITTING -> REVEALING -appeal-fail-> ACCEPTED
        -appeal-> COMMITTING -> REVEALING -appeal-success->
        PENDING -> PROPOSING -> COMMITTING -> REVEALING -> ACCEPTED -> -no-appeal-> FINALIZED
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
        for i in range(37)
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
            Leader agrees + 10 validators agree.
            Appeal: 13 validators agree. So appeal fails.
            Appeal: 25 validators disagree. So appeal succeeds.
            Leader agrees + 34 validators agree.
            """
            if len(created_nodes) < 5:
                vote = Vote.AGREE
            elif (len(created_nodes) >= 5) and (len(created_nodes) < 5 + 7):
                vote = Vote.DISAGREE
            elif (len(created_nodes) >= 5 + 7) and (
                len(created_nodes) < 5 + 7 + 11 + 13
            ):
                vote = Vote.AGREE
            elif (len(created_nodes) >= 5 + 7 + 11 + 13) and (
                len(created_nodes) < 5 + 7 + 11 + 13 + 25
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

    expected_nb_created_nodes = DEFAULT_VALIDATORS_COUNT
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

    # Appeal successful
    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == False
    )

    timestamp_awaiting_finalization_1 = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["timestamp_awaiting_finalization"]

    transactions_processor.set_transaction_appeal(transaction.hash, True)
    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == True
    )

    time.sleep(2)

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

    time.sleep(2)

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

    n_new = expected_nb_created_nodes - 1
    expected_nb_created_nodes += n_new
    assert len(created_nodes) == expected_nb_created_nodes

    timestamp_awaiting_finalization_2 = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["timestamp_awaiting_finalization"]

    assert timestamp_awaiting_finalization_2 > timestamp_awaiting_finalization_1

    assert (
        len(
            transactions_processor.get_transaction_by_hash(transaction.hash)[
                "consensus_data"
            ]["validators"]
        )
        == n_new - 1
    )

    new_leader_address = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["consensus_data"]["leader_receipt"]["node_config"]["address"]

    assert new_leader_address != old_leader_address
    assert new_leader_address in validator_set_addresses

    # Appeal fails
    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == False
    )

    transactions_processor.set_transaction_appeal(transaction.hash, True)
    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == True
    )

    time.sleep(2)

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
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
        ]
    }

    expected_nb_created_nodes += n_new + 2
    assert len(created_nodes) == expected_nb_created_nodes

    assert (
        len(
            transactions_processor.get_transaction_by_hash(transaction.hash)[
                "consensus_data"
            ]["validators"]
        )
        == 2 * n_new + 1
    )

    timestamp_awaiting_finalization_3 = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["timestamp_awaiting_finalization"]

    assert timestamp_awaiting_finalization_3 == timestamp_awaiting_finalization_2

    validator_set_addresses_after_appeal_fail = {
        validator["node_config"]["address"]
        for validator in transactions_processor.get_transaction_by_hash(
            transaction.hash
        )["consensus_data"]["validators"]
    }

    # Appeal successful
    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == False
    )

    transactions_processor.set_transaction_appeal(transaction.hash, True)
    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
        == True
    )

    time.sleep(2)

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
            TransactionStatus.ACCEPTED,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.PENDING,
        ]
    }

    expected_nb_created_nodes += 2 * n_new + 3
    assert len(created_nodes) == expected_nb_created_nodes

    transaction_dict = transactions_processor.get_transaction_by_hash(transaction.hash)
    validator_set_addresses = {
        validator["node_config"]["address"]
        for validator in transaction_dict["consensus_data"]["validators"]
    }
    old_leader_address = transaction_dict["consensus_data"]["leader_receipt"][
        "node_config"
    ]["address"]

    assert validator_set_addresses_after_appeal_fail.issubset(validator_set_addresses)

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
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.PENDING,
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
            TransactionStatus.ACCEPTED,
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

    expected_nb_created_nodes += 3 * n_new + 2
    assert len(created_nodes) == expected_nb_created_nodes

    timestamp_awaiting_finalization_4 = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["timestamp_awaiting_finalization"]

    assert timestamp_awaiting_finalization_4 > timestamp_awaiting_finalization_3

    assert (
        len(
            transactions_processor.get_transaction_by_hash(transaction.hash)[
                "consensus_data"
            ]["validators"]
        )
        == 3 * n_new + 1
    )

    new_leader_address = transactions_processor.get_transaction_by_hash(
        transaction.hash
    )["consensus_data"]["leader_receipt"]["node_config"]["address"]

    assert new_leader_address != old_leader_address
    assert new_leader_address in validator_set_addresses


@pytest.mark.asyncio
async def test_exec_undetermined_appeal(managed_thread):
    """
    Test that a transaction can be appealed when it is in the undetermined state. This verifies that:
    1. The transaction can enter appeal state after being in the undetermined state
    2. New validators are selected to process the appeal and the old leader is removed
    3. All possible path regarding undetermined appeals are correctly handled.
    4. The transaction is finalized after the appeal window
    The transaction flow:
        UNDETERMINED -appeal-fail-> UNDETERMINED
        -appeal-success-after-3-rounds-> ACCEPTED
        -successful-appeal-> PENDING -> UNDETERMINED -appeal-success-> FINALIZED
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
            "stake": 1,
            "provider": f"provider{i}",
            "model": f"model{i}",
            "config": f"config{i}",
        }
        for i in range(
            2 * (2 * (2 * (2 * DEFAULT_VALIDATORS_COUNT + 1) + 1) + 1) + 1 + 4
        )
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
            Leader disagrees + 4 validators disagree for 5 rounds
            Appeal leader fails: leader disagrees + 10 validators disagree for 11 rounds
            Appeal leader succeeds: leader disagrees + 22 validators disagree for 2 rounds then agree for 1 round

            Appeal validator succeeds: 25 validators disagree
            Leader disagrees + 46 validators disagree. -> 47 rounds
            Appeal leader fails: leader disagrees + 94 validators disagree. -> 95 rounds
            """
            n_first = DEFAULT_VALIDATORS_COUNT
            n_second = 2 * n_first + 1
            n_third = 2 * n_second + 1
            nb_first_agree = (n_first**2) + (n_second**2) + (n_third * 2)
            if (len(created_nodes) >= nb_first_agree) and (
                len(created_nodes) < nb_first_agree + n_third
            ):
                return Vote.AGREE
            else:
                return Vote.DISAGREE

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

    def appeal():
        assert (
            transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
            == False
        )
        transactions_processor.set_transaction_appeal(transaction.hash, True)
        assert (
            transactions_processor.get_transaction_by_hash(transaction.hash)["appeal"]
            == True
        )
        time.sleep(1)

    def check_validator_count(n):
        assert (
            len(
                transactions_processor.get_transaction_by_hash(transaction.hash)[
                    "consensus_data"
                ]["validators"]
            )
            == n - 1  # -1 because of the leader
        )

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

    for node in created_nodes:
        node.exec_transaction.assert_awaited_once_with(transaction)

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.UNDETERMINED.value
    )
    transaction_history = [
        *[
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
        ]
        * DEFAULT_VALIDATORS_COUNT,
        TransactionStatus.UNDETERMINED,
    ]
    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": transaction_history
    }

    nb_validators = DEFAULT_VALIDATORS_COUNT
    nb_created_nodes = DEFAULT_VALIDATORS_COUNT**2
    check_validator_count(nb_validators)
    assert len(created_nodes) == nb_created_nodes

    appeal()

    transaction_dict = transactions_processor.get_transaction_by_hash(transaction.hash)
    transaction = Transaction.from_dict(transaction_dict)
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
    transaction_history += [
        TransactionStatus.PENDING,
        *[
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
        ]
        * (2 * DEFAULT_VALIDATORS_COUNT + 1),
        TransactionStatus.UNDETERMINED,
    ]
    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": transaction_history
    }

    nb_validators += nb_validators + 1
    nb_created_nodes += nb_validators**2
    check_validator_count(nb_validators)
    assert len(created_nodes) == nb_created_nodes

    appeal()

    transaction_dict = transactions_processor.get_transaction_by_hash(transaction.hash)
    transaction = Transaction.from_dict(transaction_dict)
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
    transaction_history += [
        TransactionStatus.PENDING,
        *[
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
        ]
        * 3,
        TransactionStatus.ACCEPTED,
    ]
    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": transaction_history
    }

    nb_validators += nb_validators + 1
    nb_created_nodes += nb_validators * 3
    check_validator_count(nb_validators)
    assert len(created_nodes) == nb_created_nodes

    appeal()

    assert (
        transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
        == TransactionStatus.PENDING.value
    )
    transaction_history += [
        TransactionStatus.COMMITTING,
        TransactionStatus.REVEALING,
        TransactionStatus.PENDING,
    ]
    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": transaction_history
    }

    nb_created_nodes += nb_validators + 2
    nb_validators += nb_validators + 2
    check_validator_count(nb_validators)
    assert len(created_nodes) == nb_created_nodes

    transaction_dict = transactions_processor.get_transaction_by_hash(transaction.hash)
    transaction = Transaction.from_dict(transaction_dict)
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
    transaction_history += [
        *[
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
        ]
        * (2 * (2 * (2 * DEFAULT_VALIDATORS_COUNT + 1) + 1) + 1),
        TransactionStatus.UNDETERMINED,
    ]
    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": transaction_history
    }

    nb_validators -= 1
    nb_created_nodes += nb_validators**2
    check_validator_count(nb_validators)
    assert len(created_nodes) == nb_created_nodes

    appeal()

    transaction_dict = transactions_processor.get_transaction_by_hash(transaction.hash)
    transaction = Transaction.from_dict(transaction_dict)
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
    transaction_history += [
        TransactionStatus.PENDING,
        *[
            TransactionStatus.PROPOSING,
            TransactionStatus.COMMITTING,
            TransactionStatus.REVEALING,
        ]
        * (2 * (2 * (2 * (2 * DEFAULT_VALIDATORS_COUNT + 1) + 1) + 1) + 1),
        TransactionStatus.UNDETERMINED,
        TransactionStatus.FINALIZED,
    ]
    assert transactions_processor.updated_transaction_status_history == {
        "transaction_hash": transaction_history
    }

    nb_validators += nb_validators + 1
    nb_created_nodes += nb_validators**2
    check_validator_count(nb_validators)
    assert len(created_nodes) == nb_created_nodes
