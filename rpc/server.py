# rpc/server.py

import os
import json
import psycopg2
import string
import requests

from database.credentials import get_genlayer_db_connection
from database.functions import DatabaseFunctions
from database.helpers import convert_to_dict
from database.types import ContractData, CallContractInputData
from consensus.algorithm import exec_transaction
from consensus.utils import vrf, genvm_url
from rpc.address_utils import address_is_in_correct_format, create_new_address


@jsonrpc.method("send_transaction")  # DB
def send_transaction(from_account: str, to_account: str, amount: float) -> dict:
    msg = MessageHandler(app, socketio)

    if not address_is_in_correct_format(from_account):
        return msg.error_response(message="from_account not in ethereum address format")

    if not address_is_in_correct_format(to_account):
        return msg.error_response(message="to_account not in ethereum address format")

    try:
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
            cursor.execute(
                "SELECT data FROM current_state WHERE id = %s;", (to_account,)
            )
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
                "INSERT INTO transactions (from_address, to_address, value, type) VALUES (%s, %s, %s, %s, 0) RETURNING *;",
                (from_account, to_account, amount),
            )

            new_transaction = cursor.fetchone()

            new_transaction_dict = convert_to_dict(cursor, new_transaction)

            cursor.execute(
                "INSERT INTO transactions_audit (transaction_id, data) VALUES (%s, %s);",
                (
                    new_transaction_dict["id"],
                    json.dumps(new_transaction_dict),
                ),
            )

            connection.commit()
            cursor.close()
            connection.close()
        else:
            return msg.error_response(message="insufficient funds")

    except Exception as e:
        return msg.error_response(exception=e)

    return msg.success_response(
        {"from_account": from_account, "to_account": to_account, "amount": amount}
    )


@jsonrpc.method("deploy_intelligent_contract")  # genvm
def deploy_intelligent_contract(
    from_account: str, class_name: str, contract_code: str, constructor_args: str
) -> dict:
    msg = MessageHandler(app, socketio)

    if not address_is_in_correct_format(from_account):
        return msg.error_response(message="from_account not in ethereum address format")

    with DatabaseFunctions() as dbf:
        all_validators = dbf.all_validators()
        dbf.close()

    # Select validators using VRF
    num_validators = int(os.environ["NUMVALIDATORS"])
    selected_validators = vrf(all_validators, num_validators)

    leader_config = selected_validators[0]

    payload = {
        "jsonrpc": "2.0",
        "method": "deploy_contract",
        "params": [
            from_account,
            contract_code,
            constructor_args,
            class_name,
            leader_config,
        ],
        "id": 3,
    }
    response = requests.post(genvm_url() + "/api", json=payload).json()

    if response["result"]["status"] == "error":
        return msg.response_format(**response["result"])

    try:
        connection = get_genlayer_db_connection()
        cursor = connection.cursor()
        contract_id = create_new_address()
        contract_data = ContractData(
            code=contract_code, state=response["result"]["data"]["contract_state"]
        ).model_dump_json()
        try:
            cursor.execute(
                "INSERT INTO current_state (id, data) VALUES (%s, %s);",
                (contract_id, contract_data),
            )
            cursor.execute(
                "INSERT INTO transactions (from_address, to_address, data, type) VALUES (%s, %s, %s, 1) RETURNING *;",
                (from_account, contract_id, contract_data),
            )

            new_transaction = cursor.fetchone()

            new_transaction_dict = convert_to_dict(cursor, new_transaction)

            cursor.execute(
                "INSERT INTO transactions_audit (transaction_id, data) VALUES (%s, %s);",
                (
                    new_transaction_dict["id"],
                    json.dumps(new_transaction_dict),
                ),
            )
        except psycopg2.errors.UndefinedTable:
            return msg.error_response(message="create the tables in the database first")
        except psycopg2.errors.InFailedSqlTransaction:
            return msg.error_response(message="create the tables in the database first")

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        return msg.error_response(exception=e)

    return msg.success_response({"contract_id": contract_id})


@jsonrpc.method("count_validators")  # DB
def count_validators() -> dict:
    msg = MessageHandler(app, socketio)

    try:
        connection = get_genlayer_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT count(*) FROM validators;")

        row = cursor.fetchone()

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        return msg.error_response(exception=e)

    return msg.success_response({"count": row[0]})


@jsonrpc.method("call_contract_function")  # DB
async def call_contract_function(
    from_address: str, contract_address: str, function_name: str, args: list
) -> dict:
    msg = MessageHandler(app, socketio)

    if not address_is_in_correct_format(from_address):
        return msg.error_response(message="from_address not in ethereum address format")

    if not address_is_in_correct_format(contract_address):
        return msg.error_response(
            message="contract_address not in ethereum address format"
        )

    try:
        connection = get_genlayer_db_connection()
        cursor = connection.cursor()
        msg.info_response("db connection created")

        function_call_data = CallContractInputData(
            contract_address=contract_address, function_name=function_name, args=args
        ).model_dump_json()
        msg.info_response("Data formatted")

        msg.info_response(
            f"Transaction sent from {from_address} to {contract_address}..."
        )

        # TODO: More logging needs to be done inside the consensus functionallity
        # call consensus
        execution_output = await exec_transaction(
            from_address, json.loads(function_call_data), logger=log_status
        )

        cursor.close()
        connection.close()
        msg.info_response("db closed")

    except Exception as e:
        return msg.error_response(exception=e)

    return msg.success_response({"execution_output": execution_output})


@jsonrpc.method("get_last_contracts")  # DB
def get_last_contracts(number_of_contracts: int) -> dict:
    msg = MessageHandler(app, socketio)

    try:
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
            contract_info = {"address": contract[0]}
            contracts_info.append(contract_info)

            cursor.close()
            connection.close()

    except Exception as e:
        return msg.error_response(exception=e)

    return msg.success_response(contracts_info)


@jsonrpc.method("get_contract_state")  # DB
def get_contract_state(
    contract_address: str, method_name: str, method_args: list
) -> dict:
    msg = MessageHandler(app, socketio)

    try:
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
            return msg.error_response(
                message=contract_address + " contract does not exist"
            )

        code = row[0][1]["code"]
        state = row[0][1]["state"]
        payload = {
            "jsonrpc": "2.0",
            "method": "get_contract_data",
            "params": [code, state, method_name, method_args],
            "id": 4,
        }
        result = requests.post(genvm_url() + "/api", json=payload).json()["result"]

        if result["status"] == "error":
            return msg.error_response(result["message"])

        response = {"id": row[0][0]}
        response[method_name] = result["data"]

    except Exception as e:
        return msg.error_response(exception=e)

    return msg.success_response(response)


@jsonrpc.method("get_icontract_schema")  # DB
def get_icontract_schema(contract_address: str) -> dict:
    msg = MessageHandler(app, socketio)

    try:
        connection = get_genlayer_db_connection()
        cursor = connection.cursor()

        # Query the database for the current state of a deployed contract
        cursor.execute(
            "SELECT * FROM transactions WHERE to_address = %s AND type = 1;",
            (contract_address,),
        )
        tx = cursor.fetchone()

        if not tx:
            return msg.error_response(
                message=contract_address + " contract does not exist"
            )

        # 4 = data
        tx_contract = tx[4]

        if not tx_contract:
            return msg.error_response(
                message="contract" + contract_address + " does not contain any data"
            )

        if "code" not in tx_contract:
            return msg.error_response(
                message="contract"
                + contract_address
                + " does not contain any contract code"
            )

        contract = tx_contract["code"]

    except Exception as e:
        return msg.error_response(exception=e)

    payload = {
        "jsonrpc": "2.0",
        "method": "get_icontract_schema",
        "params": [contract],
        "id": 2,
    }

    data = requests.post(genvm_url() + "/api", json=payload).json()["result"]

    return msg.response_format(**data)


@jsonrpc.method("get_icontract_schema_for_code")  # genvm
def get_icontract_schema_for_code(contract_code: str) -> dict:
    msg = MessageHandler(app, socketio)

    payload = {
        "jsonrpc": "2.0",
        "method": "get_icontract_schema",
        "params": [contract_code],
        "id": 2,
    }

    data = requests.post(genvm_url() + "/api", json=payload).json()["result"]

    return msg.response_format(**data)


from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_socketio import SocketIO
from flask_cors import CORS
from message_handler.base import MessageHandler
from rpc.endpoints import register_all_rpc_endpoints
from dotenv import load_dotenv


def create_app():
    app = Flask("jsonrpc_api")
    CORS(app, resources={r"/api/*": {"origins": "*"}}, intercept_exceptions=False)
    jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)
    socketio = SocketIO(app, cors_allowed_origins="*")
    msg_handler = MessageHandler(app, socketio)
    return app, jsonrpc, socketio, msg_handler


if __name__ == "__main__":
    load_dotenv()
    app, jsonrpc, socketio, msg_handler = create_app()
    register_all_rpc_endpoints(app, jsonrpc, msg_handler)

    socketio.run(
        app,
        debug=os.environ["VSCODEDEBUG"] == "false",
        port=os.environ.get("RPCPORT"),
        host="0.0.0.0",
        allow_unsafe_werkzeug=True,
    )
