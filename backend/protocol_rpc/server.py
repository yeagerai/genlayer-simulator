# rpc/server.py

import os
import threading

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
from backend.consensus.base import ConsensusAlgorithm

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
    state_db_service = StateDBService(genlayer_db_client)
    state_domain = State(
        state_db_service,
        transactions_db_service,
        validators_db_service,
    )
    consensus = ConsensusAlgorithm(state_domain)
    return (
        app,
        jsonrpc,
        socketio,
        msg_handler,
        state_domain,
        validators_domain,
        consensus,
    )


load_dotenv()
app, jsonrpc, socketio, msg_handler, state_domain, validators_domain, consensus = (
    create_app()
)
register_all_rpc_endpoints(app, jsonrpc, msg_handler, state_domain, validators_domain)


def run_socketio():
    socketio.run(
        app,
        debug=os.environ["VSCODEDEBUG"] == "false",
        port=os.environ.get("RPCPORT"),
        host="0.0.0.0",
        allow_unsafe_werkzeug=True,
    )


def run_crawl_snapshot():
    consensus.crawl_snapshot()


def run_consensus_algorithm():
    consensus.run_consensus()


# Thread for the Flask-SocketIO server
thread_socketio = threading.Thread(target=run_socketio)
thread_socketio.start()

# Thread for the crawl_snapshot method
thread_crawl_snapshot = threading.Thread(target=run_crawl_snapshot)
thread_crawl_snapshot.start()

# Thread for the run_consensus method
thread_consensus = threading.Thread(target=run_consensus_algorithm)
thread_consensus.start()

# Join threads to the main thread to keep them running
thread_socketio.join()
thread_crawl_snapshot.join()
thread_consensus.join()
