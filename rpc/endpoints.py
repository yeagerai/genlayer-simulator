# rpc/endpoints.py

import random
from functools import partial
import json
from database.functions import DatabaseFunctions
from database.init_db import (
    create_db_if_it_doesnt_already_exists as create_db,
    create_tables_if_they_dont_already_exist as create_tables,
    clear_db_tables as clear_account_and_transactions_tables,
)

from node.nodes.create_nodes import (
    get_default_config_for_providers_and_nodes,
    get_providers,
    get_provider_models,
)
from node.nodes.create_nodes import random_validator_config
from node.domain.state import State as StateDomain
from node.domain.validators import Validators as ValidatorsDomain

from rpc.address_utils import create_new_address
from rpc.endpoint_generator import generate_rpc_endpoint
from rpc.address_utils import address_is_in_correct_format, create_new_address
from rpc.errors import InvalidAddressError, ItemNotFoundError, InvalidInputError


def ping() -> dict:
    return {"status": "OK"}


def create_account(state_domain: StateDomain) -> dict:
    account_address = create_new_address()
    state_domain.create_account(account_address)
    return {"account_address": account_address}


def fund_account(
    state_domain: StateDomain, account_address: str, amount: float
) -> dict:
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
    state_domain: StateDomain,
    from_address: str,
    contract_address: str,
    function_name: str,
    args: dict,
) -> dict:
    if not address_is_in_correct_format(from_address):
        raise InvalidAddressError(from_address)
    if not address_is_in_correct_format(contract_address):
        raise InvalidAddressError(contract_address)

    return state_domain.call_contract_function(
        from_address, contract_address, function_name, args
    )


def get_all_validators(validators_domain: ValidatorsDomain) -> dict:
    return validators_domain.get_all_validators()


def get_validator(validators_domain: ValidatorsDomain, validator_address: str) -> dict:
    return validators_domain.get_validator(validator_address)


def create_validator(
    validators_domain: ValidatorsDomain,
    stake: float,
    provider: str,
    model: str,
    config: dict,
) -> dict:
    new_address = create_new_address()
    new_validator = {
        "address": new_address,
        "stake": stake,
        "provider": provider,
        "model": model,
        "config": json.dumps(config),
    }
    return validators_domain.create_validator(new_validator)


def update_validator(
    validators_domain: ValidatorsDomain,
    validator_address: str,
    stake: float,
    provider: str,
    model: str,
    config: dict,
) -> dict:
    validator = get_validator(validator_address)
    if validator is None:
        raise ItemNotFoundError(validator_address, "Validator not found")

    validator["stake"] = stake
    validator["provider"] = provider
    validator["model"] = model
    validator["config"] = json.dumps(config)
    return validators_domain.update_validator(validator)


def delete_validator(
    validators_domain: ValidatorsDomain, validator_address: str
) -> dict:
    validator = get_validator(validator_address)
    if validator is None:
        raise ItemNotFoundError(validator_address, "Validator not found")

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


def create_random_validators(
    count: int, min_stake: float, max_stake: float, providers: list = []
) -> dict:
    for _ in range(count):
        stake = random.uniform(min_stake, max_stake)
        details = random_validator_config(providers=providers)
        new_validator = create_validator(
            stake, details["provider"], details["model"], details["config"]
        )
        if new_validator["status"] == "error":
            raise SystemError("Failed to create Validator")
    response = get_all_validators()
    return response


def create_random_validator(stake: float) -> dict:
    details = random_validator_config()
    response = create_validator(
        stake, details["provider"], details["model"], details["config"]
    )
    return response


def count_validators(validators_domain: ValidatorsDomain) -> dict:
    return validators_domain.count_validators()


def register_all_rpc_endpoints(
    app, jsonrpc, msg_handler, state_domain, validators_domain
):
    register_rpc_endpoint = partial(generate_rpc_endpoint, jsonrpc, msg_handler)

    register_rpc_endpoint(ping)
    register_rpc_endpoint(create_db)
    register_rpc_endpoint(partial(validators_domain, create_validator))
    register_rpc_endpoint(partial(validators_domain, update_validator))
    register_rpc_endpoint(partial(validators_domain, delete_validator))
    register_rpc_endpoint(partial(validators_domain, get_validator))
    register_rpc_endpoint(partial(validators_domain, delete_all_validators))
    register_rpc_endpoint(partial(validators_domain, get_all_validators))
    register_rpc_endpoint(create_random_validator)
    register_rpc_endpoint(create_random_validators)
    register_rpc_endpoint(partial(create_tables, app))
    register_rpc_endpoint(get_providers_and_models)
    register_rpc_endpoint(
        partial(
            clear_account_and_transactions_tables, ["current_state", "transactions"]
        )
    )
    register_rpc_endpoint(partial(create_account, state_domain))
    register_rpc_endpoint(partial(fund_account, state_domain))
    register_rpc_endpoint(partial(send_transaction, state_domain))
    register_rpc_endpoint(partial(deploy_intelligent_contract, state_domain))
    register_rpc_endpoint(partial(get_last_contracts, state_domain))
    register_rpc_endpoint(partial(call_contract_function, state_domain))
