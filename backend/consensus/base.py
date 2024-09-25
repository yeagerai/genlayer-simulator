# backend/consensus/base.py

DEFAULT_VALIDATORS_COUNT = 5
DEFAULT_CONSENSUS_SLEEP_TIME = 5

import asyncio
from collections import deque
import traceback
from typing import Any, Callable, Iterator

from backend.consensus.vrf import get_validators_for_transaction
from backend.database_handler.chain_snapshot import ChainSnapshot
from backend.database_handler.contract_snapshot import ContractSnapshot
from backend.database_handler.db_client import DBClient
from backend.database_handler.transactions_processor import (
    TransactionsProcessor,
    TransactionStatus,
)
from backend.database_handler.accounts_manager import AccountsManager
from backend.database_handler.types import ConsensusData
from backend.domain.types import (
    Transaction,
    TransactionType,
    transaction_from_dict,
    LLMProvider,
    Validator,
)
from backend.node.base import Node
from backend.node.genvm.types import ExecutionMode, Receipt, Vote
from backend.protocol_rpc.message_handler.base import (
    LogEvent,
    EventType,
    EventScope,
    MessageHandler,
)


def node_factory(
    validator: dict,
    validator_mode: ExecutionMode,
    contract_snapshot: ContractSnapshot,
    leader_receipt: Receipt | None,
    msg_handler: MessageHandler,
) -> Node:
    return Node(
        contract_snapshot=contract_snapshot,
        validator_mode=validator_mode,
        leader_receipt=leader_receipt,
        msg_handler=msg_handler,
        validator=Validator(
            address=validator["address"],
            stake=validator["stake"],
            llmprovider=LLMProvider(
                provider=validator["provider"],
                model=validator["model"],
                config=validator["config"],
                plugin=validator["plugin"],
                plugin_config=validator["plugin_config"],
            ),
        ),
    )


class ConsensusAlgorithm:
    def __init__(
        self,
        dbclient: DBClient,
        msg_handler: MessageHandler,
    ):
        self.dbclient = dbclient
        self.msg_handler = msg_handler
        self.queues: dict[str, asyncio.Queue] = {}

    def run_crawl_snapshot_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._crawl_snapshot())
        loop.close()

    async def _crawl_snapshot(self):
        while True:
            with self.dbclient.get_session() as session:
                chain_snapshot = ChainSnapshot(session)
                pending_transactions = chain_snapshot.get_pending_transactions()
                for transaction in pending_transactions:
                    transaction = transaction_from_dict(transaction)
                    address = transaction.to_address or transaction.from_address

                    if address not in self.queues:
                        self.queues[address] = asyncio.Queue()
                    await self.queues[address].put(transaction)
            await asyncio.sleep(DEFAULT_CONSENSUS_SLEEP_TIME)

    def run_consensus_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._run_consensus())
        loop.close()

    async def _run_consensus(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        # watch out! as ollama uses GPU resources and webrequest aka selenium uses RAM
        # TODO: async sessions would be a good idea to not block the current thread
        while True:
            try:
                async with asyncio.TaskGroup() as tg:
                    for queue in [q for q in self.queues.values() if not q.empty()]:
                        # sessions cannot be shared between coroutines, we need to create a new session for each coroutine
                        # https://docs.sqlalchemy.org/en/20/orm/session_basics.html#is-the-session-thread-safe-is-asyncsession-safe-to-share-in-concurrent-tasks
                        transaction = await queue.get()
                        with self.dbclient.get_session() as session:
                            tg.create_task(
                                self.exec_transaction(
                                    transaction,
                                    TransactionsProcessor(session, self.msg_handler),
                                    ChainSnapshot(session),
                                    AccountsManager(session),
                                    lambda contract_address, session=session: ContractSnapshot(
                                        contract_address, session
                                    ),
                                )
                            )

            except Exception as e:
                print("Error running consensus", e)
                print(traceback.format_exc())
            await asyncio.sleep(DEFAULT_CONSENSUS_SLEEP_TIME)

    async def exec_transaction(
        self,
        transaction: Transaction,
        transactions_processor: TransactionsProcessor,
        snapshot: ChainSnapshot,
        accounts_manager: AccountsManager,
        contract_snapshot_factory: Callable[[str], ContractSnapshot],
        node_factory: Callable[
            [
                dict,
                ExecutionMode,
                ContractSnapshot,
                Receipt | None,
                MessageHandler,
            ],
            Node,
        ] = node_factory,
    ):
        if (
            transactions_processor.get_transaction_by_hash(transaction.hash)["status"]
            != TransactionStatus.PENDING.value
        ):
            # This is a patch for a TOCTOU problem we have https://github.com/yeagerai/genlayer-simulator/issues/387
            # Problem: Pending transactions are checked by `_crawl_snapshot`, which appends them to queues. These queues are consumed by `_run_consensus`, which processes the transactions. This means that a transaction can be processed multiple times, since `_crawl_snapshot` can append the same transaction to the queue multiple times.
            # Partial solution: This patch checks if the transaction is still pending before processing it. This is not the best solution, but we'll probably refactor the whole consensus algorithm in the short term.
            print(" ~ ~ ~ ~ ~ TRANSACTION ALREADY IN PROCESS: ", transaction)
            return

        print(" ~ ~ ~ ~ ~ EXECUTING TRANSACTION: ", transaction)

        # If transaction is a transfer, execute it
        # TODO: consider when the transfer involves a contract account, bridging, etc.
        if transaction.type == TransactionType.SEND:
            return self.execute_transfer(
                transaction, transactions_processor, accounts_manager
            )

        # Select Leader and validators
        all_validators = snapshot.get_all_validators()
        involved_validators = get_validators_for_transaction(
            all_validators, DEFAULT_VALIDATORS_COUNT
        )

        for validators in rotate(involved_validators):
            # Update transaction status
            transactions_processor.update_transaction_status(
                transaction.hash, TransactionStatus.PROPOSING
            )

            [leader, *remaining_validators] = validators

            num_validators = len(remaining_validators) + 1

            contract_snapshot = contract_snapshot_factory(transaction.to_address)

            # Create Leader
            leader_node = node_factory(
                leader,
                ExecutionMode.LEADER,
                contract_snapshot,
                None,
                self.msg_handler,
            )

            # Leader executes transaction
            leader_receipt = await leader_node.exec_transaction(transaction)
            votes = {leader["address"]: leader_receipt.vote.value}
            # Update transaction status
            transactions_processor.update_transaction_status(
                transaction.hash, TransactionStatus.COMMITTING
            )

            # Create Validators
            validator_nodes = [
                node_factory(
                    validator,
                    ExecutionMode.VALIDATOR,
                    contract_snapshot,
                    leader_receipt,
                    self.msg_handler,
                )
                for validator in remaining_validators
            ]

            # Validators execute transaction
            validation_tasks = [
                (
                    validator.exec_transaction(transaction)
                )  # watch out! as ollama uses GPU resources and webrequest aka selenium uses RAM
                for validator in validator_nodes
            ]
            validation_results = await asyncio.gather(*validation_tasks)

            for i, validation_result in enumerate(validation_results):
                votes[validator_nodes[i].address] = validation_result.vote.value
            transactions_processor.update_transaction_status(
                transaction.hash,
                TransactionStatus.REVEALING,
            )

            if (
                len([vote for vote in votes.values() if vote == Vote.AGREE.value])
                >= num_validators // 2
            ):
                break  # Consensus reached

            print(
                "Consensus not reached for transaction, rotating leader: ", transaction
            )

        else:  # this block is executed if the loop above is not broken
            print("Consensus not reached for transaction: ", transaction)
            transactions_processor.update_transaction_status(
                transaction.hash, TransactionStatus.UNDETERMINED
            )
            return

        transactions_processor.update_transaction_status(
            transaction.hash, TransactionStatus.ACCEPTED
        )

        final = False
        consensus_data = ConsensusData(
            final=final,
            votes=votes,
            leader_receipt=leader_receipt,
            validators=validation_results,
        ).to_dict()

        self.msg_handler.send_message(
            LogEvent(
                "consensus_data_updated",
                EventType.INFO,
                EventScope.CONSENSUS,
                "Updated consensus data",
                consensus_data,
            )
        )

        # Register contract if it is a new contract
        if transaction.type == TransactionType.DEPLOY_CONTRACT:
            new_contract = {
                "id": transaction.data["contract_address"],
                "data": {
                    "state": leader_receipt.contract_state,
                    "code": transaction.data["contract_code"],
                },
            }
            contract_snapshot.register_contract(new_contract)

            self.msg_handler.send_message(
                LogEvent(
                    "deployed_contract",
                    EventType.SUCCESS,
                    EventScope.GENVM,
                    "Contract deployed",
                    new_contract,
                )
            )

        # Update contract state if it is an existing contract
        else:
            contract_snapshot.update_contract_state(leader_receipt.contract_state)

        # Finalize transaction
        transactions_processor.set_transaction_result(
            transaction.hash,
            consensus_data,
        )

    def execute_transfer(
        self,
        transaction: Transaction,
        transactions_processor: TransactionsProcessor,
        accounts_manager: AccountsManager,
    ):

        # TODO: dispatch event
        """
        Executes a native token transfer between Externally Owned Accounts (EOAs).

        This function handles the transfer of native tokens from one EOA to another.
        It updates the balances of both the sender and recipient accounts, and
        manages the transaction status throughout the process.

        Args:
            transaction (dict): The transaction details including from_address, to_address, and value.
            transactions_processor (TransactionsProcessor): Processor to update transaction status.
            accounts_manager (AccountsManager): Manager to handle account balance updates.
        """

        # If from_address is None, it is a fund_account call
        if not transaction.from_address is None:
            # Get the balance of the sender account
            from_balance = accounts_manager.get_account_balance(
                transaction.from_address
            )

            # If the sender does not have enough balance, set the transaction status to UNDETERMINED
            if from_balance < transaction.value:
                transactions_processor.update_transaction_status(
                    transaction.hash, TransactionStatus.UNDETERMINED
                )
                return

            # Update the balance of the sender account
            accounts_manager.update_account_balance(
                transaction.from_address, from_balance - transaction.value
            )

        # If to_address is None, it is a burn call
        if not transaction.to_address is None:
            to_balance = accounts_manager.get_account_balance(transaction.to_address)

            # Update the balance of the recipient account
            accounts_manager.update_account_balance(
                transaction.to_address, to_balance + transaction.value
            )

        transactions_processor.update_transaction_status(
            transaction.hash, TransactionStatus.FINALIZED
        )


def rotate(nodes: list) -> Iterator[list]:
    nodes = deque(nodes)
    for _ in range(len(nodes)):
        yield list(nodes)
        nodes.rotate(-1)
