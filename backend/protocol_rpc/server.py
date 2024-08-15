# backend/protocol_rpc/server.py

import os
import threading

from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_socketio import SocketIO
from flask_cors import CORS
from backend.protocol_rpc.configuration import GlobalConfiguration
from backend.protocol_rpc.message_handler.base import MessageHandler
from backend.protocol_rpc.endpoints import register_all_rpc_endpoints
from dotenv import load_dotenv

from backend.database_handler.db_client import DBClient
from backend.database_handler.transactions_processor import TransactionsProcessor
from backend.database_handler.validators_registry import ValidatorsRegistry
from backend.database_handler.accounts_manager import AccountsManager
from backend.consensus.base import ConsensusAlgorithm


def create_app():
    app = Flask("jsonrpc_api")
    CORS(app, resources={r"/api/*": {"origins": "*"}}, intercept_exceptions=False)
    jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)
    socketio = SocketIO(app, cors_allowed_origins="*")
    msg_handler = MessageHandler(app, socketio)
    genlayer_db_client = DBClient("genlayer")
    transactions_processor = TransactionsProcessor(genlayer_db_client)
    accounts_manager = AccountsManager(genlayer_db_client, transactions_processor)
    validators_registry = ValidatorsRegistry(genlayer_db_client)

    consensus = ConsensusAlgorithm(
        genlayer_db_client, transactions_processor, msg_handler
    )
    return (
        app,
        jsonrpc,
        socketio,
        msg_handler,
        genlayer_db_client,
        accounts_manager,
        transactions_processor,
        validators_registry,
        consensus,
    )


load_dotenv()
(
    app,
    jsonrpc,
    socketio,
    msg_handler,
    genlayer_db_client,
    accounts_manager,
    transactions_processor,
    validators_registry,
    consensus,
) = create_app()
register_all_rpc_endpoints(
    jsonrpc,
    msg_handler,
    genlayer_db_client,
    accounts_manager,
    transactions_processor,
    validators_registry,
    config=GlobalConfiguration(),
)


def run_socketio():
    socketio.run(
        app,
        debug=os.environ["VSCODEDEBUG"] == "false",
        port=os.environ.get("RPCPORT"),
        host="0.0.0.0",
        allow_unsafe_werkzeug=True,
    )


# Thread for the Flask-SocketIO server
thread_socketio = threading.Thread(target=run_socketio)
thread_socketio.start()

# Thread for the crawl_snapshot method
thread_crawl_snapshot = threading.Thread(target=consensus.run_crawl_snapshot_loop)
thread_crawl_snapshot.start()

# Thread for the run_consensus method
thread_consensus = threading.Thread(target=consensus.run_consensus_loop)
thread_consensus.start()
