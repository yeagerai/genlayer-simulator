from contextlib import redirect_stdout
from dataclasses import asdict
import io
import json
import base64
from typing import Callable, Optional

from backend.domain.types import Validator, Transaction, TransactionType
from backend.node.genvm.base import GenVM
from backend.database_handler.contract_snapshot import ContractSnapshot
from backend.node.genvm.types import Receipt, ExecutionMode, Vote
from backend.protocol_rpc.message_handler.base import MessageHandler


class Node:
    def __init__(
        self,
        contract_snapshot: ContractSnapshot,
        validator_mode: ExecutionMode,
        validator: Validator,
        contract_snapshot_factory: Callable[[str], ContractSnapshot],
        leader_receipt: Optional[Receipt] = None,
        msg_handler: MessageHandler = None,
    ):
        self.validator_mode = validator_mode
        self.address = validator.address
        self.leader_receipt = leader_receipt
        self.msg_handler = msg_handler
        self.contract_snapshot_factory = contract_snapshot_factory
        self.genvm = GenVM(
            contract_snapshot,
            self.validator_mode,
            validator.to_dict(),
            contract_snapshot_factory,
            msg_handler,
        )

    async def exec_transaction(self, transaction: Transaction) -> Receipt:
        transaction_data = transaction.data
        if transaction.type == TransactionType.DEPLOY_CONTRACT:
            calldata = base64.b64decode(transaction_data["calldata"])
            receipt = await self.deploy_contract(
                transaction.from_address,
                transaction_data["contract_code"],
                calldata,
            )
        elif transaction.type == TransactionType.RUN_CONTRACT:
            calldata = base64.b64decode(transaction_data["calldata"])
            receipt = await self.run_contract(
                transaction.from_address,
                calldata,
            )
        else:
            receipt = ...
        return receipt

    def parse_transaction_execution_receipt(self, receipt: Receipt) -> Receipt:
        if (
            self.validator_mode == ExecutionMode.LEADER
            or self.leader_receipt.contract_state == receipt.contract_state
        ):
            receipt.vote = Vote.AGREE

        else:
            receipt.vote = Vote.DISAGREE

        return receipt

    async def deploy_contract(
        self,
        from_address: str,
        code_to_deploy: str,
        calldata: bytes,
    ) -> Receipt:
        receipt = await self.genvm.deploy_contract(
            from_address, code_to_deploy, calldata, self.leader_receipt
        )
        return self.parse_transaction_execution_receipt(receipt)

    async def run_contract(self, from_address: str, calldata: bytes) -> Receipt:
        receipt = await self.genvm.run_contract(
            from_address, calldata, self.leader_receipt
        )

        return self.parse_transaction_execution_receipt(receipt)

    def get_contract_data(
        self,
        code: str,
        state: str,
        calldata: bytes,
    ):
        result = self.genvm.get_contract_data(
            code,
            state,
            calldata,
            self.contract_snapshot_factory,
        )

        return result

    def get_contract_schema(self, code: str):
        return GenVM.get_contract_schema(code)
