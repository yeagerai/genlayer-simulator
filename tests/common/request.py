# tests/common/request.py
import os
import json
import requests
import time
from dotenv import load_dotenv
from eth_account import Account

from tests.common.transactions import sign_transaction, encode_transaction_data

load_dotenv()


def payload(function_name: str, *args) -> dict:
    return {
        "jsonrpc": "2.0",
        "method": function_name,
        "params": [*args],
        "id": 1,
    }


def post_request(
    payload: dict,
    protocol: str = os.environ["RPCPROTOCOL"],
    host: str = os.environ["RPCHOST"],
    port: str = os.environ["RPCPORT"],
):
    return requests.post(
        protocol + "://" + host + ":" + port + "/api",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    )


def post_request_localhost(payload: dict):
    return post_request(payload, "http", "localhost")


def get_transaction_by_id(transaction_id: str):
    payload_data = payload("get_transaction_by_id", transaction_id)
    raw_response = post_request_localhost(payload_data)
    return raw_response.json()


def call_contract_method(
    contract_address: str,
    from_account: Account,
    method_name: str,
    method_args: list,
):
    params_as_string = json.dumps(method_args)
    encoded_data = encode_transaction_data([method_name, params_as_string])
    return post_request_localhost(
        payload("call", contract_address, from_account.address, encoded_data)
    ).json()


def send_transaction(
    account: Account,
    contract_address: str,
    method_name: str,
    method_args: list,
    value: int = 0,
):
    call_data = (
        None
        if method_name is None and method_args is None
        else [method_name, json.dumps(method_args)]
    )
    signed_transaction = sign_transaction(account, call_data, contract_address, value)
    return send_raw_transaction(signed_transaction)


def deploy_intelligent_contract(
    account: Account, contract_code: str, constructor_params: str
):
    deploy_data = [contract_code, constructor_params]
    signed_transaction = sign_transaction(account, deploy_data)
    return send_raw_transaction(signed_transaction)


def send_raw_transaction(signed_transaction: str):
    payload_data = payload("send_raw_transaction", signed_transaction)
    raw_response = post_request_localhost(payload_data)
    call_method_response = raw_response.json()
    if not call_method_response["result"]:
        raise ValueError("No result found in the call_method_response")
    transaction_id = call_method_response["result"]["data"]["transaction_id"]

    transaction_response = wait_for_transaction(transaction_id)
    return (call_method_response, transaction_response)


def wait_for_transaction(transaction_id: str, interval: int = 10, retries: int = 15):
    attempts = 0
    while attempts < retries:
        transaction_response = get_transaction_by_id(str(transaction_id))
        status = transaction_response["result"]["data"]["status"]
        if status == "FINALIZED":
            return transaction_response
        time.sleep(interval)
        attempts += 1

    raise TimeoutError(
        f"Transaction {transaction_id} not finalized after {retries} retries"
    )
