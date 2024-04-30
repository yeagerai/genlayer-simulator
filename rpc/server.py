import os
import re
import json
import psycopg2
import random
import string
import requests
from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_socketio import SocketIO
from flask_cors import CORS

from database.init_db import (
    create_db_if_it_doesnt_already_exists,
    create_tables_if_they_dont_already_exist,
    clear_db_tables,
)
from database.credentials import get_genlayer_db_connection
from database.functions import DatabaseFunctions
from database.types import ContractData, CallContractInputData
from consensus.algorithm import exec_transaction
from consensus.utils import genvm_url
from consensus.nodes.create_nodes import random_validator_config

from dotenv import load_dotenv

load_dotenv()

app = Flask("jsonrpc_api")

CORS(app, resources={r"/api/*": {"origins": "*"}}, intercept_exceptions=False)
jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


def log_status(message):
    socketio.emit("status_update", {"message": message})


def create_new_address() -> str:
    new_address = "".join(random.choice(string.hexdigits) for _ in range(40))
    return "0x" + new_address


def address_is_in_correct_format(address: str) -> bool:
    pattern = r"^0x[" + string.hexdigits + "]{40}$"
    if re.fullmatch(pattern, address):
        return True
    return False


@jsonrpc.method("create_db")
def create_db() -> dict:
    result = create_db_if_it_doesnt_already_exists()
    app.logger.info(result)
    return {"status": result}


@jsonrpc.method("create_tables")
def create_tables() -> dict:
    result = create_tables_if_they_dont_already_exist(app)
    app.logger.info(result)
    return {"status": result}

@jsonrpc.method("clear_tables")
def clear_tables() -> dict:
    result = clear_db_tables()
    app.logger.info(result)
    return {"status": result}


@jsonrpc.method("create_account")
def create_account() -> dict:
    balance = 0
    new_address = create_new_address()

    connection = get_genlayer_db_connection()
    cursor = connection.cursor()

    account_state = json.dumps({"balance": balance})

    cursor.execute(
        "INSERT INTO current_state (id, data) VALUES (%s, %s);",
        (new_address, account_state),
    )
    return {"address": new_address, "balance": balance, "status": "account created"}


@jsonrpc.method("fund_account")
def fund_account(account: string, balance: float) -> dict:

    if not address_is_in_correct_format(account):
        return {"status": "account not in ethereum address format"}

    connection = get_genlayer_db_connection()
    cursor = connection.cursor()

    current_account = account
    if account == "create_account":
        current_account = create_account()
    account_state = json.dumps({"balance": balance})

    # Update current_state table with the new account and its balance
    cursor.execute(
        "INSERT INTO current_state (id, data) VALUES (%s, %s);",
        (current_account, account_state),
    )

    # Optionally log the account creation in the transactions table
    cursor.execute(
        "INSERT INTO transactions (from_address, to_address, data, value, type) VALUES (NULL, %s, %s, %s, 0);",
        (
            current_account,
            json.dumps({"action": "create_account", "initial_balance": balance}),
            balance,
        ),
    )

    connection.commit()
    cursor.close()
    connection.close()
    return {"address": current_account, "balance": balance, "status": "account funded"}


@jsonrpc.method("send_transaction")
def send_transaction(from_account: str, to_account: str, amount: float) -> dict:

    if not address_is_in_correct_format(from_account):
        return {"status": "from_account not in ethereum address format"}

    if not address_is_in_correct_format(to_account):
        return {"status": "to_account not in ethereum address format"}
    connection = get_genlayer_db_connection()
    cursor = connection.cursor()

    # Verify sender's balance
    cursor.execute("SELECT data FROM current_state WHERE id = %s;", (from_account,))
    sender_state = cursor.fetchone()
    if sender_state and sender_state[0].get("balance", 0) >= amount:
        # Update sender's balance
        new_sender_balance = sender_state[0]["balance"] - amount
        cursor.execute(
            "UPDATE current_state SET data = jsonb_set(data, '{balance}', %s) WHERE id = %s;",
            (json.dumps(new_sender_balance), from_account),
        )

        # Update recipient's balance
        cursor.execute("SELECT data FROM current_state WHERE id = %s;", (to_account,))
        recipient_state = cursor.fetchone()
        if recipient_state:
            new_recipient_balance = recipient_state[0].get("balance", 0) + amount
            cursor.execute(
                "UPDATE current_state SET data = jsonb_set(data, '{balance}', %s) WHERE id = %s;",
                (json.dumps(new_recipient_balance), to_account),
            )
        else:
            # Create account if it doesn't exist
            cursor.execute(
                "INSERT INTO current_state (id, data) VALUES (%s, %s);",
                (to_account, json.dumps({"balance": amount})),
            )

        # Log the transaction
        cursor.execute(
            "INSERT INTO transactions (from_address, to_address, value, type) VALUES (%s, %s, %s, %s, 0);",
            (from_account, to_account, amount),
        )
        connection.commit()
        status = "success"
    else:
        status = "failure: insufficient funds"

    cursor.close()
    connection.close()
    return {"status": status}


@jsonrpc.method("deploy_intelligent_contract")
def deploy_intelligent_contract(
    from_account: str, contract_code: str, initial_state: str
) -> dict:

    if not address_is_in_correct_format(from_account):
        return {"status": "from_account not in ethereum address format"}

    connection = get_genlayer_db_connection()
    cursor = connection.cursor()
    contract_id = create_new_address()
    contract_data = ContractData(
        code=contract_code, state=json.loads(initial_state)
    ).model_dump_json()
    try:
        cursor.execute(
            "INSERT INTO current_state (id, data) VALUES (%s, %s);",
            (contract_id, contract_data),
        )
        cursor.execute(
            "INSERT INTO transactions (from_address, to_address, data, type) VALUES (%s, %s, %s, 1);",
            (from_account, contract_id, contract_data),
        )
    except psycopg2.errors.UndefinedTable:
        app.logger.error("create the tables in the database first")
    except psycopg2.errors.InFailedSqlTransaction:
        app.logger.error("create the tables in the database first")

    connection.commit()
    cursor.close()
    connection.close()

    log_status(f"Intelligent Contract deployed ID: {contract_id}")
    return {"status": "deployed", "contract_id": contract_id}


@jsonrpc.method("count_validators")
def count_validators() -> dict:
    connection = get_genlayer_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT count(*) FROM validators;")

    row = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return {"count": row[0]}


@jsonrpc.method("get_validator")
def get_validator(validator_address: str) -> dict:
    with DatabaseFunctions() as dbf:
        validator = dbf.get_validator(validator_address)
        dbf.close()

    if len(validator) > 0:
        return {"status": "success", "message": "", "data": validator}
    else:
        return {"status": "error", "message": "validator not found", "data": {}}


@jsonrpc.method("get_all_validators")
def get_all_validators() -> dict:
    with DatabaseFunctions() as dbf:
        validators = dbf.all_validators()
        dbf.close()

    return {"status": "success", "message": "", "data": validators}


@jsonrpc.method("create_validator")
def create_validator(stake: float, provider: str, model: str, config: json) -> dict:
    new_address = create_new_address()
    config_json = json.dumps(config)
    with DatabaseFunctions() as dbf:
        dbf.create_validator(new_address, stake, provider, model, config_json)
        dbf.close()
    return get_validator(new_address)


@jsonrpc.method("update_validator")
def update_validator(
    validator_address: str, stake: float, provider: str, model: str, config: json
) -> dict:
    validator = get_validator(validator_address)
    if validator["status"] == "error":
        return validator
    config_json = json.dumps(config)
    with DatabaseFunctions() as dbf:
        dbf.update_validator(validator_address, stake, provider, model, config_json)
        dbf.close()
    return get_validator(validator_address)


@jsonrpc.method("delete_validator")
def delete_validator(validator_address: str) -> dict:
    validator = get_validator(validator_address)
    if validator["status"] == "error":
        return validator
    with DatabaseFunctions() as dbf:
        dbf.delete_validator(validator_address)
        dbf.close()

    return {"status": "success", "message": "", "data": {"address": validator_address}}


@jsonrpc.method("delete_all_validators")
def delete_all_validators() -> dict:
    all_validators = get_all_validators()
    data = all_validators["data"]
    addresses = []
    with DatabaseFunctions() as dbf:
        for validator in data:
            addresses.append(validator["address"])
            dbf.delete_validator(validator["address"])
        dbf.close()
    return get_all_validators()

@jsonrpc.method("create_random_validators")
def create_random_validator(count:int, min_stake:float, max_stake:float) -> list:
    responses = []
    for _ in range(count):
        stake = random.uniform(min_stake, max_stake)
        details = random_validator_config()
        new_validator = create_validator(stake, details["provider"], details["model"], details["config"])
        responses.append(new_validator)
    return responses

@jsonrpc.method("create_random_validator")
def create_random_validator(stake: float) -> dict:
    details = random_validator_config()
    return create_validator(
        stake, details["provider"], details["model"], details["config"]
    )


# TODO: DEPRECIATED
@jsonrpc.method("register_validator")
def register_validator(stake: float) -> dict:
    connection = get_genlayer_db_connection()
    cursor = connection.cursor()

    eoa_id = create_new_address()
    eoa_state = json.dumps({"staked_balance": stake})

    cursor.execute(
        "INSERT INTO current_state (id, data) VALUES (%s, %s);", (eoa_id, eoa_state)
    )

    config = json.dumps({"eoa_id": eoa_id, "stake": stake})
    cursor.execute(
        "INSERT INTO validators (stake, config) VALUES (%s, %s);",
        (stake, config),
    )

    connection.commit()
    cursor.close()
    connection.close()
    return {"validator_id": eoa_id, "stake": stake, "status": "registered"}


@jsonrpc.method("call_contract_function")
async def call_contract_function(
    from_account: str, contract_address: str, function_name: str, args: list
) -> dict:

    if not address_is_in_correct_format(from_account):
        return {"status": "from_account not in ethereum address format"}

    if not address_is_in_correct_format(contract_address):
        return {"status": "contract_address not in ethereum address format"}

    connection = get_genlayer_db_connection()
    cursor = connection.cursor()

    function_call_data = CallContractInputData(
        contract_address=contract_address, function_name=function_name, args=args
    ).model_dump_json()

    cursor.execute(
        "INSERT INTO transactions (from_address, to_address, input_data, type, created_at) VALUES (%s, %s, %s, 2, CURRENT_TIMESTAMP);",
        (from_account, contract_address, function_call_data),
    )

    connection.commit()
    log_status(f"Transaction sent from {from_account} to {contract_address}...")

    # call consensus
    execution_output = await exec_transaction(
        json.loads(function_call_data), logger=log_status
    )

    cursor.close()
    connection.close()
    return {
        "status": "success",
        "message": f"Function '{function_name}' called on contract at {contract_address} with args {args}.",
        "execution_output": execution_output,
    }


@jsonrpc.method("get_last_contracts")
def get_last_contracts(number_of_contracts: int) -> list:
    connection = get_genlayer_db_connection()
    cursor = connection.cursor()

    # Query the database for the last N deployed contracts
    cursor.execute(
        "SELECT to_address, data FROM transactions WHERE type = 1 ORDER BY created_at DESC LIMIT %s;",
        (number_of_contracts,),
    )
    contracts = cursor.fetchall()

    # Format the result
    contracts_info = []
    for contract in contracts:
        contract_info = {"contract_id": contract[0]}
        contracts_info.append(contract_info)

    cursor.close()
    connection.close()

    return contracts_info


@jsonrpc.method("get_contract_state")
def get_contract_state(contract_address: str) -> dict:
    connection = get_genlayer_db_connection()
    cursor = connection.cursor()

    # Query the database for the current state of a deployed contract
    cursor.execute(
        "SELECT id, data FROM current_state WHERE id = %s;", (contract_address,)
    )
    row = cursor.fetchall()
    cursor.close()
    connection.close()

    if not row:
        raise Exception(contract_address + " contract does not exist")

    return {"id": row[0][0], "data": row[0][1]}


@jsonrpc.method("get_icontract_schema")
def get_icontract_schema(contract_address: str) -> dict:
    connection = get_genlayer_db_connection()
    cursor = connection.cursor()

    # Query the database for the current state of a deployed contract
    cursor.execute(
        "SELECT * FROM transactions WHERE to_address = %s AND type = 1;",
        (contract_address,),
    )
    tx = cursor.fetchone()

    if not tx:
        raise Exception(contract_address + " contract does not exist")

    # 4 = data
    if not tx[4]:
        raise Exception("contract" + contract_address + " does not contain any data")

    tx_contract = tx[4]

    if "code" not in tx_contract:
        raise Exception(
            "contract" + contract_address + " does not contain any contract code"
        )

    contract = tx_contract["code"]

    return get_icontract_schema_for_code(contract)


@jsonrpc.method("get_icontract_schema_for_code")
def get_icontract_schema_for_code(code: str) -> dict:

    payload = {
        "jsonrpc": "2.0",
        "method": "get_icontract_schema",
        "params": [code],
        "id": 2,
    }

    return requests.post(genvm_url() + "/api", json=payload).json()["result"]


@jsonrpc.method("ping")
def ping() -> dict:
    return {"status": "OK"}


if __name__ == "__main__":
    socketio.run(
        app,
        debug=True,
        port=os.environ.get("RPCPORT"),
        host="0.0.0.0",
        allow_unsafe_werkzeug=True,
    )
