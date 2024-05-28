# consensus/domain/state.py

import os
import json

from node.services.state_db_service import StateDBService
from node.services.transactions_db_service import TransactionsDBService
from node.services.validators_db_service import ValidatorsDBService
from node.services.genvm_service import GenVMService
from node.consensus.validators import ConsensusValidators
from node.errors import (
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
        genvm_service: GenVMService,
    ):
        self.state_db_service = state_db_service
        self.transactions_db_service = transactions_db_service
        self.validators_db_service = validators_db_service
        self.num_validators = int(os.environ["NUMVALIDATORS"])
        self.consensus_validators = consensus_validators
        self.genvm_service = genvm_service

    def create_account(self, account_address: str):
        self.state_db_service.create_new_account({"id": account_address, "balance": 0})

    def fund_account(self, account_address: str, amount: int):
        # account creation or balance update
        account_data = self.state_db_service.get_account_by_address(account_address)
        if account_data:
            # Account exists, update it
            account_data["balance"] + amount
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
        from_account_data = self.state_db_service.get_account_by_address(from_address)
        to_account_data = self.state_db_service.get_account_by_address(to_address)

        if not from_account_data:
            raise AccountNotFoundError(
                from_address, f"Account {from_address} does not exist."
            )
        if not to_account_data:
            raise AccountNotFoundError(
                to_address, f"Account {to_address} does not exist."
            )
        if from_account_data["balance"] < amount:
            raise InsufficientFundsError(
                from_address, f"Insufficient funds in account {from_address}."
            )

        # Update account balances
        from_account_data["balance"] -= amount
        to_account_data["balance"] += amount
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
        from_account_data = self.state_db_service.get_account_by_address(from_address)
        if not from_account_data:
            raise AccountNotFoundError(
                from_address, f"Account {from_address} does not exist."
            )

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
