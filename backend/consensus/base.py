# backend/consensus/base.py

DEPLOY_CONTRACTS_QUEUE_KEY = "deploy_contracts"
DEFAULT_VALIDATORS_COUNT = 5
DEFAULT_CONSENSUS_SLEEP_TIME = 5

import traceback
import asyncio
from backend.node.base import Node
from backend.database_handler.db_client import DBClient
from backend.database_handler.types import ConsensusData
from backend.consensus.vrf import get_validators_for_transaction
from backend.database_handler.chain_snapshot import ChainSnapshot
from backend.database_handler.contract_snapshot import ContractSnapshot
from backend.database_handler.transactions_processor import (
    TransactionsProcessor,
    TransactionStatus,
)
from backend.node.genvm.types import ExecutionMode, Vote
from backend.protocol_rpc.message_handler.base import MessageHandler


class ConsensusAlgorithm:
    def __init__(
        self,
        dbclient: DBClient,
        transactions_processor: TransactionsProcessor,
        msg_handler: MessageHandler,
    ):
        self.dbclient = dbclient
        self.transactions_processor = transactions_processor
        self.msg_handler = msg_handler
        self.queues = {}

    def run_crawl_snapshot_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._crawl_snapshot())
        loop.close()

    async def _crawl_snapshot(self):
        while True:
            chain_snapshot = ChainSnapshot(self.dbclient)
            pending_transactions = chain_snapshot.get_pending_transactions()
            if len(pending_transactions) > 0:
                for transaction in pending_transactions:
                    contract_address = (
                        transaction["to_address"]
                        if transaction["to_address"] is not None
                        else DEPLOY_CONTRACTS_QUEUE_KEY
                    )
                    if contract_address not in self.queues:
                        self.queues[contract_address] = asyncio.Queue()
                    await self.queues[contract_address].put(transaction)
            await asyncio.sleep(DEFAULT_CONSENSUS_SLEEP_TIME)

    def run_consensus_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._run_consensus())
        loop.close()

    async def _run_consensus(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        # watch out! as ollama uses GPU resources and webrequest aka selenium uses RAM
        while True:
            if self.queues:
                chain_snapshot = ChainSnapshot(self.dbclient)
                tasks = []

                for key in self.queues.keys():
                    if not self.queues[key].empty():
                        transaction = await self.queues[key].get()
                        tasks.append(self.exec_transaction(transaction, chain_snapshot))

                if len(tasks) > 0:
                    try:
                        await asyncio.gather(*tasks)
                    except Exception as e:
                        print("Error running consensus", e)
                        print(traceback.format_exc())
            await asyncio.sleep(DEFAULT_CONSENSUS_SLEEP_TIME)

    async def exec_transaction(
        self,
        transaction: dict,
        snapshot: ChainSnapshot,
    ) -> dict:
        print(" ~ ~ ~ ~ ~ EXECUTING TRANSACTION: ", transaction)
        # Update transaction status
        self.transactions_processor.update_transaction_status(
            transaction["id"], TransactionStatus.PROPOSING.value
        )
        # Select Leader and validators
        all_validators = snapshot.get_all_validators()
        leader, remaining_validators = get_validators_for_transaction(
            all_validators, DEFAULT_VALIDATORS_COUNT
        )
        num_validators = len(remaining_validators) + 1

        contract_address = transaction.get("to_address", None)
        contract_snapshot = ContractSnapshot(contract_address, self.dbclient)

        # Create Leader
        leader_node = Node(
            contract_snapshot=contract_snapshot,
            address=leader["address"],
            validator_mode=ExecutionMode.LEADER,
            stake=leader["stake"],
            provider=leader["provider"],
            model=leader["model"],
            config=leader["config"],
            msg_handler=self.msg_handler,
        )

        # Leader executes transaction
        leader_receipt = await leader_node.exec_transaction(transaction)
        votes = {leader["address"]: leader_receipt.vote.value}
        # Update transaction status
        self.transactions_processor.update_transaction_status(
            transaction["id"], TransactionStatus.COMMITTING.value
        )

        # Create Validators
        validator_nodes = [
            Node(
                contract_snapshot=contract_snapshot,
                address=validator["address"],
                validator_mode=ExecutionMode.VALIDATOR,
                stake=validator["stake"],
                provider=validator["provider"],
                model=validator["model"],
                config=validator["config"],
                leader_receipt=leader_receipt,
                msg_handler=self.msg_handler,
            )
            for i, validator in enumerate(remaining_validators)
        ]

        # Validators execute transaction
        validators_results = []
        validation_tasks = [
            (
                validator.exec_transaction(transaction)
            )  # watch out! as ollama uses GPU resources and webrequest aka selenium uses RAM
            for validator in validator_nodes
        ]
        validation_results = await asyncio.gather(*validation_tasks)

        for i in range(len(validation_results)):
            votes[f"{validator_nodes[i].address}"] = validation_results[i].vote.value
        self.transactions_processor.update_transaction_status(
            transaction["id"], TransactionStatus.REVEALING.value
        )

        if (
            len([vote for vote in votes.values() if vote == Vote.AGREE.value])
            < num_validators // 2
        ):
            raise Exception("Consensus not reached")

        self.transactions_processor.update_transaction_status(
            transaction["id"], TransactionStatus.ACCEPTED.value
        )

        final = False
        consensus_data = ConsensusData(
            final=final,
            votes=votes,
            leader_receipt=leader_receipt,
            validators=validators_results,
        ).to_json()

        # Register contract if it is a new contract
        if transaction["type"] == 1:
            new_contract = {
                "id": transaction["data"]["contract_address"],
                "data": {
                    "state": leader_receipt.contract_state,
                    "code": transaction["data"]["contract_code"],
                },
            }
            contract_snapshot.register_contract(new_contract)

        # Update contract state if it is an existing contract
        else:
            contract_snapshot.update_contract_state(leader_receipt.contract_state)

        # Finalize transaction
        self.transactions_processor.set_transaction_result(
            transaction["id"], consensus_data
        )
