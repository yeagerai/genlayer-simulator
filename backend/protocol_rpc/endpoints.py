# rpc/endpoints.py
import random
import json
from functools import partial
from flask_jsonrpc import JSONRPC
from sqlalchemy import Table

from backend.database_handler.db_client import DBClient
from backend.database_handler.llm_providers import LLMProviderRegistry
from backend.database_handler.models import Base
from backend.domain.types import LLMProvider
from backend.node.create_nodes.providers import validate_provider
from backend.protocol_rpc.configuration import GlobalConfiguration
from backend.protocol_rpc.message_handler.base import MessageHandler
from backend.database_handler.accounts_manager import AccountsManager
from backend.database_handler.validators_registry import ValidatorsRegistry

from backend.node.create_nodes.create_nodes import (
    random_validator_config,
)

from backend.protocol_rpc.endpoint_generator import (
    generate_rpc_endpoint,
    generate_rpc_endpoint_for_partial,
)
from backend.protocol_rpc.transactions_parser import (
    decode_signed_transaction,
    transaction_has_valid_signature,
    decode_method_call_data,
    decode_deployment_data,
)
from backend.errors.errors import InvalidAddressError, InvalidTransactionError

from backend.database_handler.transactions_processor import TransactionsProcessor
from backend.node.base import Node
from backend.node.genvm.types import ExecutionMode


####### HELPER ENDPOINTS #######
def ping() -> dict:
    return {"status": "OK"}


def clear_db_tables(db_client: DBClient, tables: list) -> dict:
    with db_client.get_session() as session:
        for table_name in tables:
            table = Table(
                table_name, Base.metadata, autoload=True, autoload_with=session.bind
            )
            session.execute(table.delete())
        session.commit()


####### ACCOUNTS ENDPOINTS #######
def get_balance(accounts_manager: AccountsManager, account_address: str) -> dict:
    if not accounts_manager.is_valid_address(account_address):
        raise InvalidAddressError(
            account_address, f"Invalid address from_address: {account_address}"
        )
    account_balance = accounts_manager.get_account_balance(account_address)
    return {"account_balance": account_balance}


def fund_account(
    accounts_manager: AccountsManager,
    transactions_processor: TransactionsProcessor,
    account_address: str,
    amount: int,
) -> dict:
    if not accounts_manager.is_valid_address(account_address):
        raise InvalidAddressError(account_address)

    transaction_id = transactions_processor.insert_transaction(
        None, account_address, None, amount, 0
    )
    return {"transaction_id": transaction_id}


####### CONTRACT CODE SCHEMA ENDPOINTS #######
def get_contract_schema(
    accounts_manager: AccountsManager,
    msg_handler: MessageHandler,
    contract_address: str,
) -> dict:
    if not accounts_manager.is_valid_address(contract_address):
        raise InvalidAddressError(
            contract_address,
            "Incorrect address format. Please provide a valid address.",
        )
    contract_account = accounts_manager.get_account_or_fail(contract_address)

    node = Node(
        contract_snapshot=None,
        address="",
        validator_mode=ExecutionMode.LEADER,
        stake=0,
        provider="",
        model="",
        config=None,
        leader_receipt=None,
        msg_handler=msg_handler,
    )
    return node.get_contract_schema(contract_account["data"]["code"])


def get_contract_schema_for_code(
    msg_handler: MessageHandler, contract_code: str
) -> dict:
    node = Node(
        contract_snapshot=None,
        address="",
        validator_mode=ExecutionMode.LEADER,
        stake=0,
        provider="",
        model="",
        config=None,
        leader_receipt=None,
        msg_handler=msg_handler,
    )
    return node.get_contract_schema(contract_code)


# TODO: these endpoints shouldn't return a `dict`, but I'm getting `TypeError: return type of dict must be a type; got NoneType instead`
def reset_defaults_llm_providers(llm_provider_registry: LLMProviderRegistry) -> dict:
    llm_provider_registry.reset_defaults()


def get_providers_and_models(llm_provider_registry: LLMProviderRegistry) -> dict:
    return llm_provider_registry.get_all()


def add_provider(llm_provider_registry: LLMProviderRegistry, params: dict) -> dict:
    provider = LLMProvider(
        provider=params["provider"],
        model=params["model"],
        config=params["config"],
    )
    validate_provider(provider)

    return llm_provider_registry.add(provider)


def edit_provider(
    llm_provider_registry: LLMProviderRegistry, id: int, params: dict
) -> dict:
    provider = LLMProvider(
        provider=params["provider"],
        model=params["model"],
        config=params["config"],
    )
    validate_provider(provider)

    llm_provider_registry.edit(id, provider)


def delete_provider(llm_provider_registry: LLMProviderRegistry, id: int) -> dict:
    llm_provider_registry.delete(id)


def create_validator(
    validators_registry: ValidatorsRegistry,
    accounts_manager: AccountsManager,
    stake: int,
    provider: str,
    model: str,
    config: json,
) -> dict:
    new_address = accounts_manager.create_new_account().address
    return validators_registry.create_validator(
        new_address, stake, provider, model, config
    )


def create_random_validator(
    validators_registry: ValidatorsRegistry,
    accounts_manager: AccountsManager,
    llm_provider_registry: LLMProviderRegistry,
    config: GlobalConfiguration,
    stake: int,
) -> dict:
    return create_random_validators(
        validators_registry,
        accounts_manager,
        llm_provider_registry,
        config,
        1,
        stake,
        stake,
    )[0]


def create_random_validators(
    validators_registry: ValidatorsRegistry,
    accounts_manager: AccountsManager,
    llm_provider_registry: LLMProviderRegistry,
    config: GlobalConfiguration,
    count: int,
    min_stake: int,
    max_stake: int,
    limit_providers: list[str] = None,
    limit_models: list[str] = None,
) -> dict:  # TODO: should return list
    limit_providers = limit_providers or []
    limit_models = limit_models or []

    details = random_validator_config(
        config.get_available_ollama_models,
        llm_provider_registry.get_all,
        limit_providers=set(limit_providers),
        limit_models=set(limit_models),
        amount=count,
    )

    response = []
    for detail in details:
        stake = random.randint(min_stake, max_stake)
        validator_address = accounts_manager.create_new_account().address

        validator = validators_registry.create_validator(
            validator_address,
            stake,
            detail.provider,
            detail.model,
            detail.config,
        )
        response.append(validator)

    return response


def update_validator(
    validators_registry: ValidatorsRegistry,
    accounts_manager: AccountsManager,
    validator_address: str,
    stake: int,
    provider: str,
    model: str,
    config: json,
) -> dict:
    # Remove validation while adding migration to update the db address
    # if not accounts_manager.is_valid_address(validator_address):
    #     raise InvalidAddressError(validator_address)
    return validators_registry.update_validator(
        validator_address, stake, provider, model, config
    )


def delete_validator(
    validators_registry: ValidatorsRegistry,
    accounts_manager: AccountsManager,
    validator_address: str,
) -> dict:
    # Remove validation while adding migration to update the db address
    # if not accounts_manager.is_valid_address(validator_address):
    #     raise InvalidAddressError(validator_address)

    validators_registry.delete_validator(validator_address)
    return validator_address


def delete_all_validators(
    validators_registry: ValidatorsRegistry,
) -> dict:
    validators_registry.delete_all_validators()
    return validators_registry.get_all_validators()


def get_all_validators(validators_registry: ValidatorsRegistry) -> dict:
    return validators_registry.get_all_validators()


def get_validator(
    validators_registry: ValidatorsRegistry, validator_address: str
) -> dict:
    return validators_registry.get_validator(validator_address)


def count_validators(validators_registry: ValidatorsRegistry) -> dict:
    return validators_registry.count_validators()


####### TRANSACTIONS ENDPOINTS #######
def get_transaction_by_id(
    transactions_processor: TransactionsProcessor, transaction_id: str
) -> dict:
    return transactions_processor.get_transaction_by_id(transaction_id)


def call(
    accounts_manager: AccountsManager,
    msg_handler: MessageHandler,
    to_address: str,
    from_address: str = "",
    input: str = "",
    # Future parameters:
    # gas: int = 0,
    # gas_price: int = 0,
    # value: int = 0,
) -> dict:
    if not accounts_manager.is_valid_address(from_address):
        raise InvalidAddressError(from_address)

    if not accounts_manager.is_valid_address(to_address):
        raise InvalidAddressError(to_address)

    decoded_data = decode_method_call_data(input)

    contract_account = accounts_manager.get_account_or_fail(to_address)
    node = Node(
        contract_snapshot=None,
        address="",
        validator_mode=ExecutionMode.LEADER,
        stake=0,
        provider="",
        model="",
        config=None,
        leader_receipt=None,
        msg_handler=msg_handler,
    )

    method_args = decoded_data.function_args
    if isinstance(method_args, str):
        try:
            method_args = json.loads(method_args)
        except json.JSONDecodeError:
            method_args = [method_args]

    return node.get_contract_data(
        code=contract_account["data"]["code"],
        state=contract_account["data"]["state"],
        method_name=decoded_data.function_name,
        method_args=method_args,
    )


def send_raw_transaction(
    transactions_processor: TransactionsProcessor,
    accounts_manager: AccountsManager,
    signed_transaction: str,
) -> dict:
    # Decode transaction
    decoded_transaction = decode_signed_transaction(signed_transaction)
    print("decoded_transaction", decoded_transaction)

    # Validate transaction
    if decoded_transaction is None:
        raise InvalidTransactionError("Invalid transaction data")

    from_address = decoded_transaction.from_address
    value = decoded_transaction.value

    if not accounts_manager.is_valid_address(from_address):
        raise InvalidAddressError(
            from_address, f"Invalid address from_address: {from_address}"
        )

    transaction_signature_valid = transaction_has_valid_signature(
        signed_transaction, decoded_transaction
    )
    if not transaction_signature_valid:
        raise InvalidTransactionError("Transaction signature verification failed")

    to_address = decoded_transaction.to_address

    transaction_data = {}
    result = {}
    transaction_type = None
    if not decoded_transaction.data:
        # Sending value transaction
        transaction_type = 0
    elif not to_address or to_address == "0x":
        # Contract deployment
        if value > 0:
            raise InvalidTransactionError("Deploy Transaction can't send value")

        decoded_data = decode_deployment_data(decoded_transaction.data)
        new_contract_address = accounts_manager.create_new_account().address

        transaction_data = {
            "contract_address": new_contract_address,
            "contract_code": decoded_data.contract_code,
            "constructor_args": decoded_data.constructor_args,
        }
        result["contract_address"] = new_contract_address
        to_address = None
        transaction_type = 1
    else:
        # Contract Call
        if not accounts_manager.is_valid_address(to_address):
            raise InvalidAddressError(
                to_address, f"Invalid address to_address: {to_address}"
            )
        decoded_data = decode_method_call_data(decoded_transaction.data)
        transaction_data = {
            "function_name": decoded_data.function_name,
            "function_args": decoded_data.function_args,
        }
        transaction_type = 2

    # Insert transaction into the database
    transaction_id = transactions_processor.insert_transaction(
        from_address, to_address, transaction_data, value, transaction_type
    )
    result["transaction_id"] = transaction_id

    return result


def register_all_rpc_endpoints(
    jsonrpc: JSONRPC,
    msg_handler: MessageHandler,
    genlayer_db_client: DBClient,
    accounts_manager: AccountsManager,
    transactions_processor: TransactionsProcessor,
    validators_registry: ValidatorsRegistry,
    llm_provider_registry: LLMProviderRegistry,
    config: GlobalConfiguration,
):
    register_rpc_endpoint = partial(generate_rpc_endpoint, jsonrpc, msg_handler, config)
    register_rpc_endpoint_for_partial = partial(
        generate_rpc_endpoint_for_partial, register_rpc_endpoint
    )

    register_rpc_endpoint(ping)
    register_rpc_endpoint_for_partial(
        clear_db_tables, genlayer_db_client, ["current_state", "transactions"]
    )

    register_rpc_endpoint_for_partial(get_balance, accounts_manager)
    register_rpc_endpoint_for_partial(
        fund_account, accounts_manager, transactions_processor
    )

    register_rpc_endpoint_for_partial(
        get_contract_schema, accounts_manager, msg_handler
    )
    register_rpc_endpoint_for_partial(get_contract_schema_for_code, msg_handler)

    register_rpc_endpoint_for_partial(get_providers_and_models, llm_provider_registry)
    register_rpc_endpoint_for_partial(
        reset_defaults_llm_providers, llm_provider_registry
    )
    register_rpc_endpoint_for_partial(add_provider, llm_provider_registry)
    register_rpc_endpoint_for_partial(edit_provider, llm_provider_registry)
    register_rpc_endpoint_for_partial(delete_provider, llm_provider_registry)
    register_rpc_endpoint_for_partial(
        create_validator, validators_registry, accounts_manager
    )
    register_rpc_endpoint_for_partial(
        create_random_validator,
        validators_registry,
        accounts_manager,
        llm_provider_registry,
        config,
    )
    register_rpc_endpoint_for_partial(
        create_random_validators,
        validators_registry,
        accounts_manager,
        llm_provider_registry,
        config,
    )
    register_rpc_endpoint_for_partial(
        update_validator, validators_registry, accounts_manager
    )
    register_rpc_endpoint_for_partial(
        delete_validator, validators_registry, accounts_manager
    )
    register_rpc_endpoint_for_partial(delete_all_validators, validators_registry)
    register_rpc_endpoint_for_partial(get_all_validators, validators_registry)
    register_rpc_endpoint_for_partial(get_validator, validators_registry)

    register_rpc_endpoint_for_partial(get_transaction_by_id, transactions_processor)
    register_rpc_endpoint_for_partial(call, accounts_manager, msg_handler)
    register_rpc_endpoint_for_partial(
        send_raw_transaction, transactions_processor, accounts_manager
    )
