# rpc/server.py

import os
import json
import psycopg2
import requests

from database.credentials import get_genlayer_db_connection
from database.functions import DatabaseFunctions
from database.helpers import convert_to_dict
from database.types import ContractData, CallContractInputData
from node.consensus.execute_transaction import exec_transaction
from node.utils import vrf, genvm_url
from rpc.address_utils import address_is_in_correct_format, create_new_address


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


from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_socketio import SocketIO
from flask_cors import CORS
from message_handler.base import MessageHandler
from rpc.endpoints import register_all_rpc_endpoints
from dotenv import load_dotenv

from database.db_client import DBClient
from node.services.state_db_service import StateDBService
from node.services.validators_db_service import ValidatorsDBService
from node.services.transactions_db_service import TransactionsDBService
from node.domain.state import State
from node.domain.validators import Validators
from node.consensus.validators import ConsensusValidators
from node.services.genvm_service import GenVMService
from node.clients.rpc_client import RPCClient


def create_app():
    GENVM_URL = (
        os.environ["GENVMPROTOCOL"]
        + "://"
        + os.environ["GENVMHOST"]
        + ":"
        + os.environ["GENVMPORT"]
    )
    app = Flask("jsonrpc_api")
    CORS(app, resources={r"/api/*": {"origins": "*"}}, intercept_exceptions=False)
    jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)
    socketio = SocketIO(app, cors_allowed_origins="*")
    msg_handler = MessageHandler(app, socketio)
    genlayer_db_client = DBClient("genlayer")
    transactions_db_service = TransactionsDBService(genlayer_db_client)
    validators_db_service = ValidatorsDBService(genlayer_db_client)
    validators_domain = Validators(validators_db_service)
    consensus_validators = ConsensusValidators()
    genvm_rpc_client = RPCClient(GENVM_URL)
    genvm_service = GenVMService(genvm_rpc_client)
    state_db_service = StateDBService(genlayer_db_client)
    state_domain = State(
        state_db_service,
        transactions_db_service,
        validators_db_service,
        consensus_validators,
        genvm_service,
    )
    return app, jsonrpc, socketio, msg_handler, state_domain, validators_domain


if __name__ == "__main__":
    load_dotenv()
    app, jsonrpc, socketio, msg_handler, state_domain, validators_domain = create_app()
    register_all_rpc_endpoints(
        app, jsonrpc, msg_handler, state_domain, validators_domain
    )

    socketio.run(
        app,
        debug=os.environ["VSCODEDEBUG"] == "false",
        port=os.environ.get("RPCPORT"),
        host="0.0.0.0",
        allow_unsafe_werkzeug=True,
    )
