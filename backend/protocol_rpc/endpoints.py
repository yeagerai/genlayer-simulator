# rpc/endpoints.py
import asyncio
import random
import json
from functools import partial
from flask_jsonrpc import JSONRPC
from flask import Flask

from backend.protocol_rpc.message_handler.base import MessageHandler
from backend.database_handler.db_client import DBClient
from backend.database_handler.snapshot import Snapshot
from backend.database_handler.domain.state import State as StateDomain
from backend.database_handler.domain.validators import Validators as ValidatorsDomain
from backend.database_handler.initialization.init_db import (
    create_db_if_it_doesnt_already_exists,
    create_tables_if_they_dont_already_exist,
    clear_db_tables,
)

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
    InvalidInputError,
)

from backend.consensus.base import consensus_algorithm


def ping() -> dict:
    return {"status": "OK"}


def create_account(state_domain: StateDomain) -> dict:
    account_address = create_new_address()
    state_domain.create_account(account_address)
    return {"account_address": account_address}


def fund_account(state_domain: StateDomain, account_address: str, amount: int) -> dict:
    if not address_is_in_correct_format(account_address):
        raise InvalidAddressError(account_address)

    state_domain.fund_account(account_address, amount)
    return {"account_address": account_address, "amount": amount}


def send_transaction(
    state_domain: StateDomain, from_account: str, to_account: str, amount: int
) -> dict:
    if not address_is_in_correct_format(from_account):
        raise InvalidAddressError(from_account)

    if not address_is_in_correct_format(to_account):
        raise InvalidAddressError(to_account)

    state_domain.send_funds(from_account, to_account, amount)

    return {"from_account": from_account, "to_account": to_account, "amount": amount}


def deploy_intelligent_contract(
    state_domain: StateDomain,
    from_account: str,
    class_name: str,
    contract_code: str,
    constructor_args: str,
) -> dict:
    if not address_is_in_correct_format(from_account):
        raise InvalidAddressError(from_account)

    contract_address = create_new_address()
    return state_domain.deploy_intelligent_contract(
        from_account,
        contract_address,
        class_name,
        contract_code,
        constructor_args,
    )


def get_last_contracts(state_domain: StateDomain, number_of_contracts: int) -> dict:
    if not number_of_contracts < 1:
        raise InvalidInputError(
            "number_of_contracts",
            number_of_contracts,
            "Number of contracts should be greater than 0.",
        )
    return state_domain.get_last_contracts(number_of_contracts)


def get_icontract_schema(state_domain: StateDomain, contract_address: str) -> dict:
    if not address_is_in_correct_format(contract_address):
        raise InvalidAddressError(
            contract_address,
            "Incorrect address format. Please provide a valid address.",
        )
    return state_domain.get_contract_schema(contract_address)


def get_icontract_schema_for_code(
    state_domain: StateDomain, contract_code: str
) -> dict:
    return state_domain.get_contract_schema_for_code(contract_code)


def call_contract_function(
    dbclient: DBClient,
    from_address: str,
    contract_address: str,
    function_name: str,
    args: dict,
) -> dict:
    if not address_is_in_correct_format(from_address):
        raise InvalidAddressError(from_address)
    if not address_is_in_correct_format(contract_address):
        raise InvalidAddressError(contract_address)

    ## prepare state
    transaction_input = dbclient.write_transaction_input(function_name, args, ...)
    snapshot = Snapshot(contract_address, dbclient)

    ## prepare transaction data
    transaction_output = asyncio.run(
        consensus_algorithm(from_address, transaction_input, snapshot)
    )

    return transaction_output


def get_contract_state(
    state_domain: StateDomain,
    contract_address: str,
    method_name: str,
    method_args: list,
) -> dict:
    if not address_is_in_correct_format(contract_address):
        raise InvalidAddressError(contract_address)

    return state_domain.get_contract_state(contract_address, method_name, method_args)


def get_all_validators(validators_domain: ValidatorsDomain) -> dict:
    return validators_domain.get_all_validators()


def get_validator(validators_domain: ValidatorsDomain, validator_address: str) -> dict:
    return validators_domain.get_validator(validator_address)


def create_validator(
    validators_domain: ValidatorsDomain,
    stake: int,
    provider: str,
    model: str,
    config: json,
) -> dict:
    new_address = create_new_address()
    return validators_domain.create_validator(
        new_address, stake, provider, model, config
    )


def update_validator(
    validators_domain: ValidatorsDomain,
    validator_address: str,
    stake: int,
    provider: str,
    model: str,
    config: json,
) -> dict:
    if not address_is_in_correct_format(validator_address):
        raise InvalidAddressError(validator_address)
    return validators_domain.update_validator(
        validator_address, stake, provider, model, config
    )


def delete_validator(
    validators_domain: ValidatorsDomain, validator_address: str
) -> dict:
    if not address_is_in_correct_format(validator_address):
        raise InvalidAddressError(validator_address)

    validators_domain.delete_validator(validator_address)
    return validator_address


def delete_all_validators(
    validators_domain: ValidatorsDomain,
) -> dict:
    validators_domain.delete_all_validators()
    return validators_domain.get_all_validators()


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
    validators_domain: ValidatorsDomain,
    count: int,
    min_stake: int,
    max_stake: int,
    providers: list = [],
) -> dict:
    for _ in range(count):
        stake = random.uniform(min_stake, max_stake)
        validator_address = create_new_address()
        details = random_validator_config(providers=providers)
        new_validator = validators_domain.create_validator(
            validator_address,
            stake,
            details["provider"],
            details["model"],
            details["config"],
        )
        if not "id" in new_validator:
            raise SystemError("Failed to create Validator")
    response = validators_domain.get_all_validators()
    return response


def create_random_validator(validators_domain: ValidatorsDomain, stake: int) -> dict:
    validator_address = create_new_address()
    details = random_validator_config()
    response = validators_domain.create_validator(
        validator_address,
        stake,
        details["provider"],
        details["model"],
        details["config"],
    )
    return response


def count_validators(validators_domain: ValidatorsDomain) -> dict:
    return validators_domain.count_validators()


def register_all_rpc_endpoints(
    app: Flask,
    jsonrpc: JSONRPC,
    msg_handler: MessageHandler,
    state_domain: StateDomain,
    validators_domain: ValidatorsDomain,
):
    register_rpc_endpoint = partial(generate_rpc_endpoint, jsonrpc, msg_handler)
    register_rpc_endpoint_for_partial = partial(
        generate_rpc_endpoint_for_partial, register_rpc_endpoint
    )

    register_rpc_endpoint(ping)
    register_rpc_endpoint(create_db_if_it_doesnt_already_exists)
    register_rpc_endpoint(get_providers_and_models)
    register_rpc_endpoint_for_partial(
        clear_db_tables, ["current_state", "transactions"]
    )
    register_rpc_endpoint_for_partial(create_validator, validators_domain)
    register_rpc_endpoint_for_partial(update_validator, validators_domain)
    register_rpc_endpoint_for_partial(delete_validator, validators_domain)
    register_rpc_endpoint_for_partial(get_validator, validators_domain)
    register_rpc_endpoint_for_partial(delete_all_validators, validators_domain)
    register_rpc_endpoint_for_partial(get_all_validators, validators_domain)
    register_rpc_endpoint_for_partial(create_random_validator, validators_domain)
    register_rpc_endpoint_for_partial(create_random_validators, validators_domain)
    register_rpc_endpoint_for_partial(create_tables_if_they_dont_already_exist, app)
    register_rpc_endpoint_for_partial(create_account, state_domain)
    register_rpc_endpoint_for_partial(fund_account, state_domain)
    register_rpc_endpoint_for_partial(send_transaction, state_domain)
    register_rpc_endpoint_for_partial(deploy_intelligent_contract, state_domain)
    register_rpc_endpoint_for_partial(get_last_contracts, state_domain)
    register_rpc_endpoint_for_partial(get_icontract_schema, state_domain)
    register_rpc_endpoint_for_partial(get_icontract_schema_for_code, state_domain)
    register_rpc_endpoint_for_partial(call_contract_function, state_domain)
    register_rpc_endpoint_for_partial(get_contract_state, state_domain)
