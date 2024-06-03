# rpc/server.py

import os

from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_socketio import SocketIO
from flask_cors import CORS
from message_handler.base import MessageHandler
from backend.protocol_rpc.endpoints import register_all_rpc_endpoints
from dotenv import load_dotenv

from backend.database_handler.db_client import DBClient
from backend.database_handler.services.state_db_service import StateDBService
from backend.database_handler.services.validators_db_service import ValidatorsDBService
from backend.database_handler.services.transactions_db_service import (
    TransactionsDBService,
)
from backend.database_handler.domain.state import State
from backend.database_handler.domain.validators import Validators
from backend.consensus.validators import ConsensusValidators

GENVM_URL = (
    os.environ["GENVMPROTOCOL"]
    + "://"
    + os.environ["GENVMHOST"]
    + ":"
    + os.environ["GENVMPORT"]
)


def create_app():
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
    state_db_service = StateDBService(genlayer_db_client)
    state_domain = State(
        state_db_service,
        transactions_db_service,
        validators_db_service,
        consensus_validators,
    )
    return app, jsonrpc, socketio, msg_handler, state_domain, validators_domain


load_dotenv()
app, jsonrpc, socketio, msg_handler, state_domain, validators_domain = create_app()
register_all_rpc_endpoints(app, jsonrpc, msg_handler, state_domain, validators_domain)

socketio.run(
    app,
    debug=os.environ["VSCODEDEBUG"] == "false",
    port=os.environ.get("RPCPORT"),
    host="0.0.0.0",
    allow_unsafe_werkzeug=True,
)
