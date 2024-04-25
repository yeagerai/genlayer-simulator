import re
import os
import json
import psycopg2
import string
import requests
import logging
import random
import inspect
from logging.config import dictConfig
from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_socketio import SocketIO
from flask_cors import CORS

from database.init_db import create_db_if_it_doesnt_already_exists, create_tables_if_they_dont_already_exist
from database.credentials import get_genlayer_db_connection
from database.types import ContractData, CallContractInputData
from consensus.algorithm import exec_transaction
from consensus.utils import genvm_url

from dotenv import load_dotenv
load_dotenv()


with open('logging_config.json', 'r') as file:
    logging_config = json.load(file)
logger = logging.getLogger(os.environ['LOGCONFIG'])

dictConfig(logging_config)


def create_new_address() -> str:
    new_address = ''.join(random.choice(string.hexdigits) for _ in range(40))
    return '0x' + new_address

def address_is_in_correct_format(address:str) -> bool:
    pattern = r'^0x['+string.hexdigits+']{40}$'
    if re.fullmatch(pattern, address):
        return True
    return False

def error_response(message:str) -> dict:
    return response_format('error', message=message)

def success_response(data) -> dict:
    return response_format('success', data=data)

def response_format(status:str, message:str='', data={}) -> dict:
    result = {
        'status': status,
        'message': message,
        'data': data
    }
    function_name = inspect.stack()[1].function
    log_status({'function': function_name, 'response': result})
    return result


app = Flask('jsonrpc_api')

CORS(app, resources={r"/api/*": {"origins": "*"}}, intercept_exceptions=False)
jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def log_status(message):
    socketio.emit('status_update', {'message': message})

@jsonrpc.method("create_db")
def create_db() -> dict:
    result = create_db_if_it_doesnt_already_exists()
    logger.info(result)
    return success_response(result)

@jsonrpc.method("create_tables")
def create_tables() -> dict:
    result = create_tables_if_they_dont_already_exist(app)
    logger.info(result)
    return success_response(result)

@jsonrpc.method("create_account")
def create_account() -> dict:
    balance = 0
    new_address = create_new_address()
    try:
        connection = get_genlayer_db_connection()
        cursor = connection.cursor()

        account_state = json.dumps({"balance": balance})

        cursor.execute(
            "INSERT INTO current_state (id, data) VALUES (%s, %s);",
            (new_address, account_state),
        )
    except Exception as e:
        logger.error(e)
        return error_response('failed to create account')
    return success_response({"address": new_address, "balance": balance})

@jsonrpc.method("fund_account")
def fund_account(account: string, balance: float) -> dict:

    if not address_is_in_correct_format(account):
        return {"status": "account not in ethereum address format"}

    try:
        connection = get_genlayer_db_connection()
        cursor = connection.cursor()

        current_account = account
        if account == 'create_account':
            current_account = create_account()

        # Update current_state table with the new account and its balance
        cursor.execute(
            "INSERT INTO current_state (id, data) VALUES (%s, %s);",
            (current_account, json.dumps({"balance": balance})),
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
    except Exception as e:
        logger.error(e)
        return error_response('failed to fund account')
    
    return success_response({"address": current_account, "balance": balance})


@jsonrpc.method("send_transaction")
def send_transaction(from_account: str, to_account: str, amount: float) -> dict:

    if not address_is_in_correct_format(from_account):
        return {"status": "from_account not in ethereum address format"}

    if not address_is_in_correct_format(to_account):
        return {"status": "to_account not in ethereum address format"}
    
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
            cursor.close()
            connection.close()
        else:
            return error_response('insufficient funds')

    except Exception as e:
        logger.error(e)
        return error_response('failed to send transaction')
    
    return success_response({
        'from_account': from_account,
        'to_account': to_account,
        'amount': amount
    })


@jsonrpc.method("deploy_intelligent_contract")
def deploy_intelligent_contract(from_account: str, contract_code: str, initial_state: str) -> dict:

    if not address_is_in_correct_format(from_account):
        return {"status": "from_account not in ethereum address format"}
    
    try:
        connection = get_genlayer_db_connection()
        cursor = connection.cursor()
        contract_id = create_new_address()
        contract_data = ContractData(code=contract_code, state=json.loads(initial_state)).model_dump_json()
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
            logger.error('create the tables in the database first')
        except psycopg2.errors.InFailedSqlTransaction:
            logger.error('create the tables in the database first')

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        logger.error(e)
        return error_response('failed to deploy contract')
    
    return success_response({'contract_id': contract_id})


@jsonrpc.method("count_validators")
def count_validators() -> dict:

    try:
        connection = get_genlayer_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT count(*) FROM validators;")

        row = cursor.fetchone()

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        logger.error(e)
        return error_response('failed to query validators')
    
    return success_response({"count": row[0]})


@jsonrpc.method("register_validator")
def register_validator(stake: float) -> dict:

    try:
        connection = get_genlayer_db_connection()
        cursor = connection.cursor()

        eoa_id = create_new_address()
        eoa_state = json.dumps({"staked_balance": stake})

        cursor.execute(
            "INSERT INTO current_state (id, data) VALUES (%s, %s);", (eoa_id, eoa_state)
        )

        validator_info = json.dumps({"eoa_id": eoa_id, "stake": stake})
        cursor.execute(
            "INSERT INTO validators (stake, validator_info) VALUES (%s, %s);",
            (stake, validator_info),
        )

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        logger.error(e)
        return error_response('failed to query validators')
    
    return success_response({"validator_id": eoa_id, "stake": stake})


@jsonrpc.method("call_contract_function")
async def call_contract_function(
    from_account: str, contract_address: str, function_name: str, args: list
) -> dict:

    if not address_is_in_correct_format(from_account):
        return {"status": "from_account not in ethereum address format"}

    if not address_is_in_correct_format(contract_address):
        return {"status": "contract_address not in ethereum address format"}

    try:
        connection = get_genlayer_db_connection()
        cursor = connection.cursor()

        function_call_data = CallContractInputData(contract_address=contract_address, function_name=function_name, args=args).model_dump_json()

        cursor.execute(
            "INSERT INTO transactions (from_address, to_address, input_data, type, created_at) VALUES (%s, %s, %s, 2, CURRENT_TIMESTAMP);",
            (from_account, contract_address, function_call_data),
        )

        connection.commit()
        log_status(f"Transaction sent from {from_account} to {contract_address}...")

        # call consensus
        execution_output = await exec_transaction(json.loads(function_call_data), logger=log_status)

        cursor.close()
        connection.close()

    except Exception as e:
        logger.error(e)
        return error_response('failed to query validators')
    
    return success_response({"execution_output": execution_output})

@jsonrpc.method("get_last_contracts")
def get_last_contracts(number_of_contracts: int) -> dict:

    try:
        connection = get_genlayer_db_connection()
        cursor = connection.cursor()

        # Query the database for the last N deployed contracts
        cursor.execute(
            "SELECT to_address, data FROM transactions WHERE type = 1 ORDER BY created_at DESC LIMIT %s;",
            (number_of_contracts,)
        )
        contracts = cursor.fetchall()

        # Format the result
        contracts_info = []
        for contract in contracts:
            contract_info = {
                "contract_id": contract[0]
            }
            contracts_info.append(contract_info)

        cursor.close()
        connection.close()

    except Exception as e:
        logger.error(e)
        return error_response('failed to query validators')
    
    return success_response(contract_info)

@jsonrpc.method("get_contract_state")
def get_contract_state(contract_address: str) -> dict:

    try:
        connection = get_genlayer_db_connection()
        cursor = connection.cursor()

        # Query the database for the current state of a deployed contract
        cursor.execute(
            "SELECT id, data FROM current_state WHERE id = %s;",
            (contract_address,)
        )
        row = cursor.fetchall()
        cursor.close()
        connection.close()
        
        if not row:
            return error_response(contract_address + ' contract does not exist')

    except Exception as e:
        logger.error(e)
        return error_response('failed to query current state')
    
    return success_response({"id": row[0][0], "data": row[0][1]})

@jsonrpc.method("get_icontract_schema")
def get_icontract_schema(contract_address: str) -> dict:

    try:
        connection = get_genlayer_db_connection()
        cursor = connection.cursor()

        # Query the database for the current state of a deployed contract
        cursor.execute(
            "SELECT * FROM transactions WHERE to_address = %s AND type = 1;",
            (contract_address,)
        )
        tx = cursor.fetchone()

        if not tx:
            return error_response(contract_address + ' contract does not exist')

        # 4 = data
        tx_contract = tx[4]

        if not tx_contract:
            return error_response('contract' + contract_address + ' does not contain any data')
        
        if 'code' not in tx_contract:
            return error_response('contract' + contract_address + ' does not contain any contract code')
        
        contract = tx_contract['code']

    except Exception as e:
        logger.error(e)
        return error_response('failed to query transactions')

    payload = {
        "jsonrpc": "2.0",
        "method": "get_icontract_schema",
        "params": [contract],
        "id": 2,
    }
    
    data = requests.post(genvm_url()+'/api', json=payload).json()['result']

    return success_response(data)


@jsonrpc.method("ping")
def ping() -> dict:
    return {"status": "OK"}

if __name__ == "__main__":
    socketio.run(app, debug=True, port=os.environ.get('RPCPORT'), host='0.0.0.0', allow_unsafe_werkzeug=True)
