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

from consensus.nodes.create_nodes import (
    get_default_config_for_providers_and_nodes,
    get_providers,
    get_provider_models,
)
from consensus.nodes.create_nodes import random_validator_config
from rpc.address_utils import create_new_address
from rpc.endpoint_generator import generate_rpc_endpoint
from rpc.address_utils import address_is_in_correct_format, create_new_address

from database import db_client
from consensus import domain
from consensus import services

genlayer_db_client = db_client.PostgresManager("genlayer")
state_db_service = services.StateDBService(genlayer_db_client)
state = domain.State(state_db_service)


def create_account() -> dict:
    account_address = create_new_address()
    state.create_account(account_address)
    return {"account_address": account_address}


def fund_account(account_address: str, amount: float) -> dict:
    if not address_is_in_correct_format(account):
        raise Exception("Incorrect address format. Please provide a valid address.")

    state.fund_account(account_address, amount)
    return {"account_address": account_address, "amount": amount}


def ping() -> dict:
    return {"status": "OK"}


def get_all_validators() -> dict:
    with DatabaseFunctions() as dbf:
        validators = dbf.all_validators()
        dbf.close()
    return validators


def get_validator(validator_address: str) -> dict:
    with DatabaseFunctions() as dbf:
        validator = dbf.get_validator(validator_address)
        dbf.close()

    if not len(validator):
        raise IndexError(validator)
    return validator


def get_providers_and_models() -> dict:
    config = get_default_config_for_providers_and_nodes()
    providers = get_providers()
    providers_and_models = {}
    for provider in providers:
        providers_and_models[provider] = get_provider_models(
            config["providers"], provider
        )
    return providers_and_models


def create_validator(stake: float, provider: str, model: str, config: dict) -> dict:
    new_address = create_new_address()
    config_json = json.dumps(config)
    with DatabaseFunctions() as dbf:
        dbf.create_validator(new_address, stake, provider, model, config_json)
        dbf.close()
    response = get_validator(new_address)
    return response


def update_validator(
    validator_address: str, stake: float, provider: str, model: str, config: dict
) -> dict:
    validator = get_validator(validator_address)
    if validator["status"] == "error":
        return validator
    config_json = json.dumps(config)
    with DatabaseFunctions() as dbf:
        dbf.update_validator(validator_address, stake, provider, model, config_json)
        dbf.close()
    response = get_validator(validator_address)
    return response


def delete_validator(validator_address: str) -> dict:
    validator = get_validator(validator_address)
    if validator["status"] == "error":
        return validator
    with DatabaseFunctions() as dbf:
        dbf.delete_validator(validator_address)
        dbf.close()
    return validator_address


def delete_all_validators() -> dict:
    all_validators = get_all_validators()
    data = all_validators["data"]
    addresses = []
    with DatabaseFunctions() as dbf:
        for validator in data:
            addresses.append(validator["address"])
            dbf.delete_validator(validator["address"])
        dbf.close()
    response = get_all_validators()
    return response


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


def register_all_rpc_endpoints(app, jsonrpc, msg_handler):
    register_rpc_endpoint = partial(generate_rpc_endpoint, jsonrpc, msg_handler)

    register_rpc_endpoint(ping)
    register_rpc_endpoint(create_validator)
    register_rpc_endpoint(update_validator)
    register_rpc_endpoint(delete_validator)
    register_rpc_endpoint(get_validator)
    register_rpc_endpoint(delete_all_validators)
    register_rpc_endpoint(create_random_validator)
    register_rpc_endpoint(create_random_validators)
    register_rpc_endpoint(get_all_validators)
    register_rpc_endpoint(create_db)
    register_rpc_endpoint(partial(create_tables, app))
    register_rpc_endpoint(get_providers_and_models)
    register_rpc_endpoint(
        partial(
            clear_account_and_transactions_tables, ["current_state", "transactions"]
        )
    )
    register_rpc_endpoint(create_account)
    register_rpc_endpoint(fund_account)
