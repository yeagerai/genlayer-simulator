import os
import sys
import ast
import subprocess
import json
import inspect
import pickle
import base64
from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_socketio import SocketIO
from flask_cors import CORS

from genvm.utils import transaction_files, save_files, delete_recipts, generate_deploy_contract, get_contract_class_name
from common.messages import MessageHandler
from common.logging import setup_logging_config

from dotenv import load_dotenv

load_dotenv()

setup_logging_config()

app = Flask("genvm_api")


CORS(app, resources={r"/api/*": {"origins": "*"}}, intercept_exceptions=False)
jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)
socketio = SocketIO(app, cors_allowed_origins="*")


@jsonrpc.method("leader_executes_transaction")
def leader_executes_transaction(contract_code: str, node_config: dict) -> dict:

    delete_recipts()

    msg = MessageHandler(app, socketio)

    icontract_file, _, _, leader_recipt_file = transaction_files()

    msg.debug_response("Contract Code", contract_code)
    msg.debug_response("Node Config", node_config)

    save_files(contract_code, node_config, "leader")

    try:
        result = subprocess.run(
            ["python", icontract_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    except Exception as e:
        return msg.error_response(exception=e)

    msg.debug_response("LLM Result", result)

    if result.returncode != 0:
        return msg.response_format(
            status="error",
            message=result.stderr.split('\n')[-2],
            data=str(result.stderr)
        )

    # Access the output of the subprocess.run command
    file = open(leader_recipt_file, "r")
    contents = json.load(file)
    file.close()

    # TODO: Leader needs to be the name of the VM
    msg.debug_response("leader_executes_transaction (response)", contents)

    delete_recipts()

    return msg.success_response(contents)


@jsonrpc.method("validator_executes_transaction")
def validator_executes_transaction(
    icontract: str, node_config: dict, leader_recipt: dict
) -> dict:

    delete_recipts()
    
    msg = MessageHandler(app, socketio)

    return_data = {"status": "error", "data": None}

    icontract_file, recipt_file, _, _ = transaction_files()

    msg.debug_response("Contract Code", icontract)
    msg.debug_response("Node Config", node_config)
    msg.debug_response("Leader Recipt", leader_recipt)

    save_files(icontract, node_config, "validator", leader_recipt)

    try:
        result = subprocess.run(
            ["python", icontract_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    except Exception as e:
        return msg.error_response(exception=e)

    msg.debug_response("LLM Result", result)

    if result.returncode != 0:
        return_data["data"] = str(result.returncode) + ": " + str(result.stderr)
        return return_data

    # Access the output of the subprocess.run command
    file = open(recipt_file, "r")
    contents = json.load(file)
    file.close()

    msg.debug_response("validator_executes_transaction (response)", contents)

    delete_recipts()

    return msg.success_response(contents)


@jsonrpc.method("get_icontract_schema")
def get_icontract_schema(icontract: str) -> dict:

    msg = MessageHandler(app, socketio)

    msg.debug_response("Contract Code", icontract)

    namespace = {}
    exec(icontract, globals(), namespace)
    class_name = get_contract_class_name(icontract)
    msg.debug_response("class name", class_name)

    if not class_name:
        return msg.error_response(message="This contract does not have a class declaration")

    iclass = namespace[class_name]

    members = inspect.getmembers(iclass)

    # Find all class methods
    methods = {}
    functions_and_methods = [
        m for m in members if inspect.isfunction(m[1]) or inspect.ismethod(m[1])
    ]
    for name, member in functions_and_methods:
        signature = inspect.signature(member)

        inputs = {}
        for method_variable_name, method_variable in signature.parameters.items():
            if method_variable_name != "self":
                annotation = str(method_variable.annotation)[8:-2]
                inputs[method_variable_name] = str(annotation)

        return_annotation = str(signature.return_annotation)[8:-2]

        if return_annotation == "inspect._empty":
            return_annotation = "None"

        result = {"inputs": inputs, "output": return_annotation}

        msg.debug_response("Class method ("+class_name+"."+name+")", result)

        methods[name] = result

    # Find all class variables
    variables = {}
    tree = ast.parse(icontract)
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for stmt in node.body:
                if isinstance(stmt, ast.AnnAssign):
                    if hasattr(stmt.annotation, "id") and hasattr(stmt.target, "id"):
                        msg.debug_response("Class variables ("+class_name+"."+stmt.target.id+")", stmt.annotation.id)
                        variables[stmt.target.id] = stmt.annotation.id

    response = {"class": class_name, "methods": methods, "variables": variables}

    return msg.success_response(response)


@jsonrpc.method("deploy_contract")
def deploy_contract(
    from_address:str, contract_code: str, constructor_args: str, class_name: str, leader_config: dict
) -> dict:
    
    msg = MessageHandler(app, socketio)

    deploy_contract_code = generate_deploy_contract(
        from_address, contract_code, constructor_args, class_name
    )

    contract_file, _, _, _ = transaction_files()
    save_files(deploy_contract_code, leader_config, "leader")

    try:
        result = subprocess.run(
            ["python", contract_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    except Exception as e:
        return msg.error_response(exception=e)

    msg.debug_response("RUN Deploy Result", result)

    if result.returncode != 0:
        return msg.error_response(message=str(result.returncode) + ": " + str(result.stderr))

    # Access the output of the subprocess.run command
    file = open(os.environ.get("GENVMCONLOC") + "/receipt_leader.json", "r")
    contents = json.load(file)
    file.close()

    msg.debug_response("Deployed contract receipt", contents)

    # os.remove(leader_recipt_file)

    return msg.success_response(contents)


@jsonrpc.method("get_contract_data")
def get_contract_data(code: str, state: str, method_name: str, method_args: list) -> dict:
    msg = MessageHandler(app, socketio)
    namespace = {}
    exec(code, namespace)

    target_module = sys.modules['__main__']
    for name, value in namespace.items():
        setattr(target_module, name, value)
    
    print("namespace", namespace)
    decoded_pickled_object = base64.b64decode(state)
    contract_state = pickle.loads(decoded_pickled_object)
    method_to_call = getattr(contract_state, method_name)
    return msg.success_response(method_to_call(*method_args))


if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get("GENVMPORT"), host="0.0.0.0")
