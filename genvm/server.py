import os
import json
import asyncio
import uuid
from flask import Flask
from flask_jsonrpc import JSONRPC

from dotenv import load_dotenv
load_dotenv()

app = Flask('genvm_api')
jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)


@jsonrpc.method("leader_executes_transaction")
def leader_executes_transaction() -> dict:
    return {"status": "Success! (1)"}

@jsonrpc.method("validator_executes_transaction")
def validator_executes_transaction() -> dict:
    return {"status": "Success! (2)"}

@jsonrpc.method("deploy_intelligent_contract")
def leader_executes_transaction() -> dict:
    return {"status": "Success! (3)"}


if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get('GENVMPORT'), host='0.0.0.0')
