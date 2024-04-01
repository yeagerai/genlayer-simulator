import os
from flask import Flask
from flask_jsonrpc import JSONRPC

from dotenv import load_dotenv
load_dotenv()

app = Flask('genvm_api')
jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)


@jsonrpc.method("leader_executes_transaction")
def leader_executes_transaction(icontract:str) -> dict:
    # TODO: Leader needs to be the name of the VM
    result = {
        "leader":"", 
        "contract_state":{}, 
        "non_det_inputs": {}, 
        "non_det_outputs":{},
        "vote":"agree"
    }
    return {"status": result}

@jsonrpc.method("validator_executes_transaction")
def validator_executes_transaction() -> dict:
    return {"status": "Success! (2)"}


if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get('GENVMPORT'), host='0.0.0.0')
