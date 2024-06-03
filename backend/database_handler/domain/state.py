# consensus/domain/state.py

import os
import json

from backend.database_handler.services.state_db_service import StateDBService
from backend.database_handler.services.transactions_db_service import (
    TransactionsDBService,
)
from backend.database_handler.services.validators_db_service import ValidatorsDBService
from backend.consensus.validators import ConsensusValidators
from backend.consensus.execute_transaction import exec_transaction
from backend.errors.errors import (
    AccountNotFoundError,
    InsufficientFundsError,
    AccountAlreadyExists,
)


class State:
    def __init__(
        self,
        state_db_service: StateDBService,
        transactions_db_service: TransactionsDBService,
        validators_db_service: ValidatorsDBService,
        consensus_validators: ConsensusValidators,
    ):
        self.state_db_service = state_db_service
        self.transactions_db_service = transactions_db_service
        self.validators_db_service = validators_db_service
        self.num_validators = int(os.environ["NUMVALIDATORS"])
        self.consensus_validators = consensus_validators

    def _get_account_or_fail(self, account_address: str):
        """Private method to check if an account exists, and raise an error if not."""
        account_data = self.state_db_service.get_account_by_address(account_address)
        if not account_data:
            raise AccountNotFoundError(
                account_address, f"Account {account_address} does not exist."
            )
        return account_data

    def create_account(self, account_address: str):
        self.state_db_service.create_new_account({"id": account_address, "balance": 0})

    def fund_account(self, account_address: str, amount: int):
        # account creation or balance update
        account_data = self.state_db_service.get_account_by_address(account_address)
        if account_data:
            # Account exists, update it
            account_data["data"]["balance"] + amount
            self.state_db_service.update_account(account_data)
        else:
            # Account doesn't exist, create it
            self.state_db_service.create_new_account(
                {"id": account_address, "balance": amount}
            )

        # Record transaction
        transaction_data = {
            "from_address": "NULL",
            "to_address": account_address,
            "data": json.dumps({"action": "fund_account", "amount": amount}),
            "value": amount,
            "type": 0,
        }
        self.transactions_db_service.insert_transaction(**transaction_data)

    def send_funds(self, from_address: str, to_address: str, amount: int):
        # account fetching and validation
        from_account_data = self._get_account_or_fail(from_address)
        to_account_data = self._get_account_or_fail(to_address)

        if from_account_data["data"]["balance"] < amount:
            raise InsufficientFundsError(
                from_address, f"Insufficient funds in account {from_address}."
            )

        # Update account balances
        from_account_data["data"]["balance"] -= amount
        to_account_data["data"]["balance"] += amount
        self.state_db_service.update_account(from_account_data)
        self.state_db_service.update_account(to_account_data)

        # Record transaction
        transaction_data = {
            "from_address": from_address,
            "to_address": to_address,
            "data": json.dumps({"action": "send_funds", "amount": amount}),
            "value": amount,
            "type": 0,
        }
        self.transactions_db_service.insert_transaction(**transaction_data)

    def deploy_intelligent_contract(
        self,
        from_address: str,
        contract_address: str,
        class_name: str,
        contract_code: str,
        constructor_args: str,
    ) -> None:
        # account fetching and validation
        self._get_account_or_fail(from_address)

        # existing contract checking
        existing_contract_account = self.state_db_service.get_account_by_address(
            contract_address
        )
        if existing_contract_account:
            raise AccountAlreadyExists(
                contract_address,
                f"Contract with address {contract_address} already exists.",
            )

        # leader selection and contract deployment
        all_validators = self.validators_db_service.get_all_validators()
        leader = self.consensus_validators.get_validators_for_transaction(
            all_validators, self.num_validators
        )

        deploy_result = self.genvm_service.deploy_contract(
            from_address, contract_code, constructor_args, class_name, leader
        )

        # Record state
        contract_data = (
            {
                "code": contract_code,
                "state": deploy_result["contract_state"],
            }
        ).model_dump_json()

        self.state_db_service.create_new_contract_account(
            contract_address, contract_data
        )
        # Record transaction
        transaction_data = {
            "from_address": from_address,
            "to_address": contract_address,
            "data": contract_data,
            "value": 0,
            "type": 1,
        }
        self.transactions_db_service.insert_transaction(**transaction_data)
        return {"contract_id": contract_address}

    def get_last_contracts(self, number_of_contracts: int) -> dict:
        last_contracts = self.state_db_service.get_last_contracts(number_of_contracts)
        return {"contracts": last_contracts}

    def get_contract_schema(self, contract_address: str) -> dict:
        contract_data = self._get_account_or_fail(contract_address)
        return self.get_contract_schema_for_code(contract_data["data"]["code"])

    def get_contract_schema_for_code(self, contract_code: str) -> dict:
        return self.genvm_service.get_contract_schema(contract_code)

    async def call_contract_function(
        self,
        from_address: str,
        contract_address: str,
        function_name: str,
        args: dict,
    ) -> dict:
        # account fetching and validation
        from_account_data = self._get_account_or_fail(from_address)
        contract_account_data = self._get_account_or_fail(contract_address)

        all_validators = self.validators_db_service.get_all_validators()
        leader, remaining_validators = (
            self.consensus_validators.get_validators_for_transaction(
                all_validators, self.num_validators
            )
        )

        # contract function call
        function_call_data = {
            "contract_address": contract_address,
            "function_name": function_name,
            "args": args,
        }
        execution_output = await exec_transaction(
            from_address,
            function_call_data,
            current_contract_state=contract_account_data["data"],
            leader=leader,
            validators=remaining_validators,
        )

        leader_data = execution_output["leader_data"]
        consensus_data = execution_output["consensus_data"]

        # Update state
        contract_data = (
            {
                "code": contract_account_data["data"]["code"],
                "state": leader_data["result"]["contract_state"],
            }
        ).model_dump_json()
        self.state_db_service.update_account(
            {"id": contract_address, "data": contract_data}
        )

        # Record transaction
        transaction_data = {
            "from_address": from_address,
            "to_address": contract_address,
            "data": json.dumps(
                {"new_contract_state": leader_data["result"]["contract_state"]}
            ),
            "consensus_data": consensus_data,
            "value": 0,
            "type": 2,
        }
        self.transactions_db_service.insert_transaction(**transaction_data)

        return {"execution_output": execution_output}

    def get_contract_state(
        self, contract_address: str, method_name: str, method_args: list
    ) -> dict:
        contract_data = self._get_account_or_fail(contract_address)
        contract_code = contract_data["data"]["code"]
        contract_state = contract_data["data"]["state"]

        result = self.genvm_service.get_contract_state(
            contract_code, contract_state, method_name, method_args
        )

        response = {"id": contract_address}
        response[method_name] = result["data"]
        return response
