import json
import traceback
from typing import Optional

from backend.node.genvm.base import GenVM
from backend.database_handler.contract_snapshot import ContractSnapshot
from backend.node.genvm.types import Receipt, ExecutionMode, Vote
from backend.protocol_rpc.message_handler.base import MessageHandler


class Node:
    def __init__(
        self,
        contract_snapshot: ContractSnapshot,
        address: str,
        validator_mode: ExecutionMode,
        stake: int,
        provider: str,
        model: str,
        config: dict,
        leader_receipt: Optional[Receipt] = None,
        msg_handler: MessageHandler = None,
    ):
        self.validator_mode = validator_mode
        self.address = address
        self.validator_info = {
            "provider": provider,
            "model": model,
            "config": config,
            "stake": stake,
        }
        self.leader_receipt = leader_receipt
        self.genvm = GenVM(
            contract_snapshot, self.validator_mode, self.validator_info, msg_handler
        )

    async def exec_transaction(self, transaction: dict):
        transaction_data = transaction["data"]
        if transaction["type"] == 1:
            receipt = self.deploy_contract(
                transaction["from_address"],
                transaction_data["contract_code"],
                transaction_data["constructor_args"],
            )
        elif transaction["type"] == 2:
            receipt = await self.run_contract(
                transaction["from_address"],
                transaction_data["function_name"],
                transaction_data["function_args"],
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

    def deploy_contract(
        self,
        from_address: str,
        code_to_deploy: str,
        constructor_args: dict,
    ):
        parsed_construction_args = json.loads(constructor_args)
        receipt = self.genvm.deploy_contract(
            from_address, code_to_deploy, parsed_construction_args
        )
        return self.parse_transaction_execution_receipt(receipt)

    async def run_contract(
        self, from_address: str, function_name: str, args: str
    ) -> dict:
        parsed_args = json.loads(args)
        receipt = await self.genvm.run_contract(
            from_address, function_name, parsed_args, self.leader_receipt
        )

        return self.parse_transaction_execution_receipt(receipt)

    def get_contract_data(
        self, code: str, state: str, method_name: str, method_args: list
    ):
        return self.genvm.get_contract_data(code, state, method_name, method_args)

    def get_contract_schema(self, code: str):
        return GenVM.get_contract_schema(code)
