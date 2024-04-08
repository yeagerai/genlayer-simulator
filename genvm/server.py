import os
import subprocess
import json
from flask import Flask
from flask_jsonrpc import JSONRPC

from dotenv import load_dotenv
load_dotenv()

app = Flask('genvm_api')
jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)


@jsonrpc.method("leader_executes_transaction")
def leader_executes_transaction(icontract:str, leader_config:dict) -> dict:

    icontract_file = os.environ.get('GENVMCONLOC') + '/icontract.py'
    recipt_file = os.environ.get('GENVMCONLOC') + '/receipt.json'
    node_config_file = os.environ.get('GENVMCONLOC') + '/node-config.json'

    with open(node_config_file, 'w') as file:
        leader_config['type'] = 'leader'
        json.dump(leader_config, file, indent=4)

    if int(os.environ.get('DEBUG')) == 1:
        print('--- START: icontract ---')
        print(icontract)
        print('--- END: icontract ---')

    with open(icontract_file, 'w+') as file:
        file.write(icontract)
    file.close()

    result = subprocess.run(['python', icontract_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if int(os.environ.get('DEBUG')) == 1:
        print('--- START: LLM Result ---')
        print(result)
        print('--- END: LLM Result ---')

        if result.returncode == 0:
            print("Command executed successfully!")
        else:
            print("Command failed with return code:", result.returncode)
            print("Stderr:", result.stderr)

    # Access the output of the command
    file = open(recipt_file, 'r')
    contents = json.load(file)

    # TODO: Leader needs to be the name of the VM
    result = {
        "leader":"", 
        "contract_state":contents['contract_state'], 
        "non_det_inputs": contents["non_det_inputs"], 
        "non_det_outputs":contents["non_det_outputs"],
        "vote":"agree"
    }
    file.close()

    return {"status": result}

@jsonrpc.method("validator_executes_transaction")
def validator_executes_transaction() -> dict:
    return {"status": "Success! (2)"}


if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get('GENVMPORT'), host='0.0.0.0')
