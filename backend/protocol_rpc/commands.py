# rpc/base.py

import json
import requests
from os import environ
from typing import IO

from dotenv import load_dotenv

load_dotenv()

json_rpc_url = (
    environ.get("RPCPROTOCOL") + "://localhost:" + environ.get("RPCPORT") + "/api"
)


def create_db_logic() -> dict:
    payload = {
        "jsonrpc": "2.0",
        "method": "create_db_if_it_doesnt_already_exists",
        "params": [],
        "id": 1,
    }
    response = requests.post(json_rpc_url, json=payload).json()
    return response


def create_tables_logic() -> dict:
    payload = {
        "jsonrpc": "2.0",
        "method": "create_tables_if_they_dont_already_exist",
        "params": [],
        "id": 1,
    }
    response = requests.post(json_rpc_url, json=payload).json()
    return response


def fund_account_logic(address: str, balance: float) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "method": "fund_account",
        "params": [address, balance],
        "id": 1,
    }
    response = requests.post(json_rpc_url, json=payload).json()
    return response


def send_logic(from_account: str, to_account: str, amount: float) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "method": "send_transaction",
        "params": [from_account, to_account, amount],
        "id": 0,
    }
    response = requests.post(json_rpc_url, json=payload).json()
    return response


def deploy_logic(
    from_account: str,
    class_name: str,
    contract_code_file: IO[bytes],
    initial_state: str,
) -> dict:
    contract_code = contract_code_file.read()

    try:
        json.loads(initial_state)
    except json.JSONDecodeError as e:
        print(f"Error parsing initial state JSON: {e}")
        return

    payload = {
        "jsonrpc": "2.0",
        "method": "deploy_intelligent_contract",
        "params": [
            from_account,
            class_name,
            contract_code.decode("utf-8"),
            initial_state,
        ],
        "id": 2,
    }
    response = requests.post(json_rpc_url, json=payload).json()
    return response


def contract_logic(
    from_account: str, contract_address: str, function: str, args: tuple
) -> dict:
    args_list = list(args)
    payload = {
        "jsonrpc": "2.0",
        "method": "call_contract_function",
        "params": [from_account, contract_address, function, args_list],
        "id": 3,
    }
    response = requests.post(json_rpc_url, json=payload).json()
    return response


def count_validators_logic() -> list:
    payload = {
        "jsonrpc": "2.0",
        "method": "count_validators",
        "params": [],
        "id": 4,
    }
    return requests.post(json_rpc_url, json=payload).json()


def create_random_validators_logic(
    count: int, min_stake: float, max_stake: float
) -> list:
    payload = {
        "jsonrpc": "2.0",
        "method": "create_random_validators",
        "params": [count, min_stake, max_stake],
        "id": 4,
    }
    responses = requests.post(json_rpc_url, json=payload).json()
    return responses


def delete_all_validators_logic() -> list:
    payload = {
        "jsonrpc": "2.0",
        "method": "delete_all_validators",
        "params": [],
        "id": 4,
    }
    responses = requests.post(json_rpc_url, json=payload).json()
    return responses
