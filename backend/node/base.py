import json
import traceback
from typing import Optional

from backend.node.genvm.base import GenVM
from backend.database_handler.contract_snapshot import ContractSnapshot


class Node:
    def __init__(
        self,
        contract_snapshot: ContractSnapshot,
        address: str,
        validator_mode: str,
        stake: int,
        provider: str,
        model: str,
        config: dict,
        leader_receipt: Optional[dict] = None,
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
        self.genvm = GenVM(contract_snapshot, self.validator_mode, self.validator_info)

    async def exec_transaction(self, transaction: dict):
        transaction_data = transaction["data"]
        if transaction["type"] == 1:
            receipt = self.deploy_contract(
                transaction["from_address"],
                transaction_data["class_name"],
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

    def deploy_contract(
        self,
        from_address: str,
        class_name: str,
        code_to_deploy: str,
        constructor_args: dict,
    ):
        receipt = None
        try:
            parsed_construction_args = json.loads(constructor_args)
            receipt = self.genvm.deploy_contract(
                class_name, from_address, code_to_deploy, parsed_construction_args
            )

        except Exception as e:
            print("Error deploying contract", e)
            print(traceback.format_exc())
            # create error receipt
        return {"vote": "agree", "result": receipt}

    async def run_contract(
        self, from_address: str, function_name: str, args: list
    ) -> dict:
        receipt = None
        try:
            receipt = await self.genvm.run_contract(
                from_address, function_name, args, self.leader_receipt
            )
        except Exception as e:
            print("Error running contract", e)
            print(traceback.format_exc())
            # create error receipt
        return {"vote": "agree", "result": receipt}

    def get_contract_data(
        self, code: str, state: str, method_name: str, method_args: list
    ):
        return GenVM.get_contract_data(code, state, method_name, method_args)

    def get_contract_schema(self, code: str):
        return GenVM.get_contract_schema(code)
