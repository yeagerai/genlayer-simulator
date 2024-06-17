from typing import Optional
from backend.node.genvm.base import GenVM

from backend.database_handler.transactions_processor import TransactionStatus


class Node:
    def __init__(
        self,
        contract_snapshot,
        address,
        validator_mode,
        config,
        leader_receipt: Optional[dict] = None,
    ):
        self.address = address
        self.validator_mode = validator_mode
        self.config = config
        self.leader_receipt = leader_receipt
        self.genvm = GenVM(contract_snapshot, self.validator_mode, self.config)

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
            receipt = self.run_contract(
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
            receipt = self.genvm.deploy_contract(
                class_name, from_address, code_to_deploy, constructor_args
            )
        except Exception as e:
            print("Error deploying contract", e)
            # create error receipt
        return {"vote": "agree", "result": receipt}

    def run_contract(self, from_address, function_name, args):
        receipt = None
        try:
            receipt = self.genvm.run_contract(
                from_address, function_name, args, self.leader_receipt
            )
        except Exception as e:
            print("Error running contract", e)
            # create error receipt
        return {"vote": "agree", "result": receipt}

    def get_contract_data(
        self, code: str, state: str, method_name: str, method_args: list
    ):
        return GenVM.get_contract_data(code, state, method_name, method_args)

    def get_contract_schema(self, code: str):
        return GenVM.get_contract_schema(code)
