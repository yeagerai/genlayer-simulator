# backend/protocol_rpc/server.py

import os
from os import environ
import threading
import logging
from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from backend.protocol_rpc.configuration import GlobalConfiguration
from backend.protocol_rpc.message_handler.base import MessageHandler
from backend.protocol_rpc.endpoints import register_all_rpc_endpoints
from dotenv import load_dotenv

from backend.database_handler.db_client import DBClient, get_db_name
from backend.database_handler.transactions_processor import TransactionsProcessor
from backend.database_handler.validators_registry import ValidatorsRegistry
from backend.database_handler.accounts_manager import AccountsManager
from backend.consensus.base import ConsensusAlgorithm
from backend.database_handler.models import Base


def create_app():

    database_name_seed = "genlayer"
    db_uri = f"postgresql+psycopg2://{environ.get('DBUSER')}:{environ.get('DBPASSWORD')}@{environ.get('DBHOST')}/{get_db_name(database_name_seed)}"
    sqlalchemy_db = SQLAlchemy(
        model_class=Base,
        session_options={
            "expire_on_commit": False
        },  # recommended in https://docs.sqlalchemy.org/en/20/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
    )

    app = Flask("jsonrpc_api")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = True
    sqlalchemy_db.init_app(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}}, intercept_exceptions=False)
    jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)
    socketio = SocketIO(app, cors_allowed_origins="*")
    msg_handler = MessageHandler(app, socketio)
    genlayer_db_client = DBClient(database_name_seed)
    transactions_processor = TransactionsProcessor(sqlalchemy_db.session)
    accounts_manager = AccountsManager(sqlalchemy_db.session)
    validators_registry = ValidatorsRegistry(sqlalchemy_db.session)

    consensus = ConsensusAlgorithm(genlayer_db_client, msg_handler)
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
    logging.getLogger("werkzeug").setLevel(
        os.environ.get("FLASK_LOG_LEVEL", logging.ERROR)
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
