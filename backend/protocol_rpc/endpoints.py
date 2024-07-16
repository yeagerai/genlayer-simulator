# rpc/endpoints.py
import asyncio
import random
import json
from functools import partial
from flask_jsonrpc import JSONRPC
from flask import Flask

from backend.database_handler.db_client import DBClient
from backend.protocol_rpc.message_handler.base import MessageHandler
from backend.database_handler.accounts_manager import AccountsManager
from backend.database_handler.validators_registry import ValidatorsRegistry

from backend.node.create_nodes.create_nodes import (
    get_default_config_for_providers_and_nodes,
    get_providers,
    get_provider_models,
    random_validator_config,
)

from backend.protocol_rpc.endpoint_generator import (
    generate_rpc_endpoint,
    generate_rpc_endpoint_for_partial,
)
from backend.protocol_rpc.address_utils import (
    address_is_in_correct_format,
    create_new_address,
)
from backend.errors.errors import (
    InvalidAddressError,
)

from backend.database_handler.transactions_processor import TransactionsProcessor
from backend.node.base import Node


def ping() -> dict:
    return {"status": "OK"}


def create_account(accounts_manager: AccountsManager) -> dict:
    account_address = create_new_address()
    accounts_manager.create_new_account(account_address, 0)
    return {"account_address": account_address}


def fund_account(
    accounts_manager: AccountsManager, account_address: str, amount: int
) -> dict:
    if not address_is_in_correct_format(account_address):
        raise InvalidAddressError(account_address)

    accounts_manager.fund_account(account_address, amount)
    return {"account_address": account_address, "amount": amount}


def send_transaction(
    transactions_processor: TransactionsProcessor,
    from_account: str,
    to_account: str,
    amount: int,
) -> dict:
    if not address_is_in_correct_format(from_account):
        raise InvalidAddressError(from_account)

    if not address_is_in_correct_format(to_account):
        raise InvalidAddressError(to_account)

    transaction_id = transactions_processor.insert_transaction(
        from_account, to_account, None, amount, 0
    )

    return {"transaction_id": transaction_id}


def deploy_intelligent_contract(
    transactions_processor: TransactionsProcessor,
    from_account: str,
    class_name: str,
    contract_code: str,
    constructor_args: str,
) -> dict:
    if not address_is_in_correct_format(from_account):
        raise InvalidAddressError(from_account)

    contract_address = create_new_address()

    transaction_data = {
        "contract_address": contract_address,
        "class_name": class_name,
        "contract_code": contract_code,
        "constructor_args": constructor_args,
    }

    transaction_id = transactions_processor.insert_transaction(
        from_account, None, transaction_data, 0, 1
    )
    return {"transaction_id": transaction_id, "contract_address": contract_address}


def call_contract_function(
    transactions_processor: TransactionsProcessor,
    from_address: str,
    contract_address: str,
    function_name: str,
    function_args: list,
) -> dict:
    if not address_is_in_correct_format(from_address):
        raise InvalidAddressError(from_address)
    if not address_is_in_correct_format(contract_address):
        raise InvalidAddressError(contract_address)

    transaction_data = {
        "function_name": function_name,
        "function_args": function_args,
    }
    transaction_id = transactions_processor.insert_transaction(
        from_address, contract_address, transaction_data, 0, 2
    )

    return {"transaction_id": transaction_id}


def get_transaction_by_id(
    transactions_processor: TransactionsProcessor, transaction_id: str
) -> dict:
    return transactions_processor.get_transaction_by_id(transaction_id)


def get_contract_schema(
    accounts_manager: AccountsManager, contract_address: str
) -> dict:
    if not address_is_in_correct_format(contract_address):
        raise InvalidAddressError(
            contract_address,
            "Incorrect address format. Please provide a valid address.",
        )
    contract_account = accounts_manager.get_account_or_fail(contract_address)

    node = Node(
        contract_snapshot=None,
        address="",
        validator_mode="leader",
        stake=0,
        provider="",
        model="",
        config=None,
        leader_receipt=None,
    )
    return node.get_contract_schema(contract_account["data"]["code"])


def get_contract_schema_for_code(contract_code: str) -> dict:
    node = Node(
        contract_snapshot=None,
        address="",
        validator_mode="leader",
        stake=0,
        provider="",
        model="",
        config=None,
        leader_receipt=None,
    )
    return node.get_contract_schema(contract_code)


def get_contract_state(
    accounts_manager: AccountsManager,
    contract_address: str,
    method_name: str,
    method_args: list,
) -> dict:
    if not address_is_in_correct_format(contract_address):
        raise InvalidAddressError(contract_address)

    contract_account = accounts_manager.get_account(contract_address)
    node = Node(
        contract_snapshot=None,
        address="",
        validator_mode="leader",
        stake=0,
        provider="",
        model="",
        config=None,
        leader_receipt=None,
    )
    return node.get_contract_data(
        code=contract_account["data"]["code"],
        state=contract_account["data"]["state"],
        method_name=method_name,
        method_args=method_args,
    )


def get_all_validators(validators_registry: ValidatorsRegistry) -> dict:
    return validators_registry.get_all_validators()


def get_validator(
    validators_registry: ValidatorsRegistry, validator_address: str
) -> dict:
    return validators_registry.get_validator(validator_address)


def create_validator(
    validators_registry: ValidatorsRegistry,
    stake: int,
    provider: str,
    model: str,
    config: json,
) -> dict:
    new_address = create_new_address()
    return validators_registry.create_validator(
        new_address, stake, provider, model, config
    )


def update_validator(
    validators_registry: ValidatorsRegistry,
    validator_address: str,
    stake: int,
    provider: str,
    model: str,
    config: json,
) -> dict:
    if not address_is_in_correct_format(validator_address):
        raise InvalidAddressError(validator_address)
    return validators_registry.update_validator(
        validator_address, stake, provider, model, config
    )


def delete_validator(
    validators_registry: ValidatorsRegistry, validator_address: str
) -> dict:
    if not address_is_in_correct_format(validator_address):
        raise InvalidAddressError(validator_address)

    validators_registry.delete_validator(validator_address)
    return validator_address


def delete_all_validators(
    validators_registry: ValidatorsRegistry,
) -> dict:
    validators_registry.delete_all_validators()
    return validators_registry.get_all_validators()


def get_providers_and_models() -> dict:
    config = get_default_config_for_providers_and_nodes()
    providers = get_providers()
    providers_and_models = {}
    for provider in providers:
        providers_and_models[provider] = get_provider_models(
            config["providers"], provider
        )
    return providers_and_models


# TODO: Refactor this function to put the random config generator inside the domain
# and reuse the generate single random validator function
def create_random_validators(
    validators_registry: ValidatorsRegistry,
    count: int,
    min_stake: int,
    max_stake: int,
    providers: list = None,
) -> dict:
    providers = providers or []

    for _ in range(count):
        stake = random.uniform(min_stake, max_stake)
        validator_address = create_new_address()
        details = random_validator_config(providers=providers)
        new_validator = validators_registry.create_validator(
            validator_address,
            stake,
            details["provider"],
            details["model"],
            details["config"],
        )
        if not "id" in new_validator:
            raise SystemError("Failed to create Validator")
    response = validators_registry.get_all_validators()
    return response


def create_random_validator(
    validators_registry: ValidatorsRegistry, stake: int
) -> dict:
    validator_address = create_new_address()
    details = random_validator_config()
    response = validators_registry.create_validator(
        validator_address,
        stake,
        details["provider"],
        details["model"],
        details["config"],
    )
    return response


def count_validators(validators_registry: ValidatorsRegistry) -> dict:
    return validators_registry.count_validators()


def clear_db_tables(db_client: DBClient, tables: list) -> dict:
    db_client.clear_tables(tables)


def register_all_rpc_endpoints(
    app: Flask,
    jsonrpc: JSONRPC,
    msg_handler: MessageHandler,
    genlayer_db_client: DBClient,
    accounts_manager: AccountsManager,
    transactions_processor: TransactionsProcessor,
    validators_registry: ValidatorsRegistry,
):
    register_rpc_endpoint = partial(generate_rpc_endpoint, jsonrpc, msg_handler)
    register_rpc_endpoint_for_partial = partial(
        generate_rpc_endpoint_for_partial, register_rpc_endpoint
    )

    register_rpc_endpoint(ping)
    register_rpc_endpoint(get_providers_and_models)
    register_rpc_endpoint(get_contract_schema_for_code)

    register_rpc_endpoint_for_partial(
        clear_db_tables, genlayer_db_client, ["current_state", "transactions"]
    )
    register_rpc_endpoint_for_partial(create_validator, validators_registry)
    register_rpc_endpoint_for_partial(update_validator, validators_registry)
    register_rpc_endpoint_for_partial(delete_validator, validators_registry)
    register_rpc_endpoint_for_partial(get_validator, validators_registry)
    register_rpc_endpoint_for_partial(delete_all_validators, validators_registry)
    register_rpc_endpoint_for_partial(get_all_validators, validators_registry)
    register_rpc_endpoint_for_partial(create_random_validator, validators_registry)
    register_rpc_endpoint_for_partial(create_random_validators, validators_registry)
    register_rpc_endpoint_for_partial(send_transaction, transactions_processor)
    register_rpc_endpoint_for_partial(
        deploy_intelligent_contract, transactions_processor
    )
    register_rpc_endpoint_for_partial(call_contract_function, transactions_processor)
    register_rpc_endpoint_for_partial(create_account, accounts_manager)
    register_rpc_endpoint_for_partial(fund_account, accounts_manager)
    register_rpc_endpoint_for_partial(get_contract_schema, accounts_manager)
    register_rpc_endpoint_for_partial(get_contract_state, accounts_manager)
    register_rpc_endpoint_for_partial(get_transaction_by_id, transactions_processor)
