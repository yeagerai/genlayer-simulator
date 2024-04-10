import os
import re
import ast
import subprocess
import json
import inspect
from flask import Flask
from flask_jsonrpc import JSONRPC

from dotenv import load_dotenv
load_dotenv()

app = Flask('genvm_api')
jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)

def debug_output(title:str, content:str):
    if int(os.environ.get('DEBUG')) == 1:
        print('--- START: '+title+' ---')
        print(content)
        print('--- END: '+title+' ---')


@jsonrpc.method("leader_executes_transaction")
def leader_executes_transaction(icontract:str, leader_config:dict) -> dict:

    icontract_file = os.environ.get('GENVMCONLOC') + '/icontract.py'
    recipt_file = os.environ.get('GENVMCONLOC') + '/receipt.json'
    node_config_file = os.environ.get('GENVMCONLOC') + '/node-config.json'

    debug_output('llm_config', leader_config)

    with open(node_config_file, 'w') as file:
        leader_config['type'] = 'leader'
        json.dump(leader_config, file, indent=4)

    debug_output('icontract', icontract)

    with open(icontract_file, 'w+') as file:
        file.write(icontract)
    file.close()

    result = subprocess.run(['python', icontract_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    debug_output('LLM Result', result)

    if result.returncode == 0:
        print("Command executed successfully!")
    else:
        print("Command failed with return code:", result.returncode)
        print("Stderr:", result.stderr)

    # Access the output of the command
    file = open(recipt_file, 'r')
    contents = json.load(file)
    debug_output('recipt.json', contents)

    # TODO: Leader needs to be the name of the VM
    result = {
        "vote":"agree",
        "node":leader_config['id'],
        "node_config":contents['node_config'],
        "contract_state":contents['contract_state'],
        "non_det_inputs": contents["non_det_inputs"], 
        "non_det_outputs":contents["non_det_outputs"]
    }
    file.close()
    debug_output('leader_executes_transaction(response)', result)

    return result
    

@jsonrpc.method("validator_executes_transaction")
def validator_executes_transaction() -> dict:
    return {"status": "Success! (2)"}


@jsonrpc.method("get_icontract_schema")
def get_icontract_schema(icontract:str) -> dict:

    debug_output('icontract', icontract)

    class_name = None
    namespace = {}
    exec(icontract, globals(), namespace)
    for class_name_in_contract, class_type_in_contract in namespace.items():
        if 'WrappedClass' in str(class_type_in_contract):
            class_name = class_name_in_contract
    
    if not class_name:
        raise Exception('This contract does not have a class declaration')

    iclass = namespace[class_name]

    members = inspect.getmembers(iclass)

    # Find all class methods
    methods = {}
    functions_and_methods = [m for m in members if inspect.isfunction(m[1]) or inspect.ismethod(m[1])]
    for name, member in functions_and_methods:
        if not name.startswith('_'):
            signature = inspect.signature(member)
            
            inputs = {}
            for method_variable_name, method_variable in signature.parameters.items():
                if method_variable_name != 'self':
                    annotation = str(method_variable.annotation)[8:-2]
                    inputs[method_variable_name] = str(annotation)
            
            return_annotation = str(signature.return_annotation)[8:-2]

            if return_annotation == 'inspect._empty':
                return_annotation = 'None'
            
            methods[name] = {'inputs': inputs, 'output':return_annotation}

    # Find all class variables
    variables = {}
    tree = ast.parse(icontract)
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for stmt in node.body:
                if isinstance(stmt, ast.AnnAssign):
                    if hasattr(stmt.annotation, 'id') and hasattr(stmt.target, 'id'):
                        variables[stmt.target.id] = stmt.annotation.id
    
    return {"class":class_name, "methods": methods, "variables": variables}


if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get('GENVMPORT'), host='0.0.0.0')
