import os
import json
import requests
import re

from dotenv import load_dotenv

load_dotenv()


def transaction_files() -> list:
    file_path = os.environ.get("GENVMCONLOC")

    icontract_file = file_path + "/icontract.py"
    recipt_file = file_path + "/receipt_validator.json"
    node_config_file = file_path + "/node-config.json"
    leader_recipt_file = file_path + "/receipt_leader.json"

    return icontract_file, recipt_file, node_config_file, leader_recipt_file


def save_files(
    contract_code: str, node_config: str, node_type: str, leader_recipt: str = None
):
    contract_code_file, _, node_config_file, leader_recipt_file = transaction_files()

    with open(node_config_file, "w") as file:
        node_config["type"] = node_type
        json.dump(node_config, file, indent=4)
    file.close()

    with open(contract_code_file, "w+") as file:
        file.write(contract_code)
    file.close()

    if leader_recipt:

        with open(leader_recipt_file, "w") as file:
            json.dump(leader_recipt, file, indent=4)
        file.close()


def delete_recipts():
    _, recipt_file, _, leader_recipt_file = transaction_files()

    for rf in [recipt_file, leader_recipt_file]:
        if os.path.exists(rf):
            os.remove(rf)


def get_webpage_content(url: str) -> str:

    payload = {
        "jsonrpc": "2.0",
        "method": "get_webpage",
        "params": [url],
        "id": 2,
    }

    result = requests.post(webrequest_url() + "/api", json=payload).json()

    if result["result"]["status"] == "error":
        raise Exception(result["result"])

    return result["result"]


def webrequest_url():
    return (
        os.environ["WEBREQUESTPROTOCOL"]
        + "://"
        + os.environ["WEBREQUESTHOST"]
        + ":"
        + os.environ["WEBREQUESTPORT"]
    )


def generate_deploy_contract(
    from_address: str,
    contract_code: str,
    constructor_args: str,
    class_name: str,
) -> str:
    return f"""
{contract_code}

current_contract = None

async def main():
    global contract_runner 
    from genvm.base.contract_runner import ContractRunner
    contract_runner = ContractRunner(from_address="{from_address}")
    contract_runner._set_mode("leader")
    import pickle
    current_contract = {class_name}(**{constructor_args})
    
    pickled_object = pickle.dumps(current_contract)
    contract_runner._write_receipt(pickled_object, '__init__', [{constructor_args}])

if __name__=="__main__":
    import asyncio
    asyncio.run(main())
"""


def get_contract_class_name(contract_code: str) -> str:
    pattern = r"class (\w+)\(IContract\):"
    matches = re.findall(pattern, contract_code)
    if len(matches) == 0:
        raise Exception("No class name found")
    return matches[0]


import os
from database.credentials import get_genlayer_db_connection
import json


def run_contract(
    from_address: str,
    contract_code: str,
    encoded_state: str,
    run_by: str,
    function_name: str,
    args_str: str,
) -> str:
    return f"""
{contract_code}

async def main():
    global contract_runner 
    from genvm.base.contract_runner import ContractRunner
    contract_runner = ContractRunner(from_address="{from_address}")
    try:
        EquivalencePrinciple.contract_runner = contract_runner
    except (ImportError, UnboundLocalError):
        from genvm.base.equivalence_principle import EquivalencePrinciple
        EquivalencePrinciple.contract_runner = contract_runner

    import pickle
    import base64
    decoded_pickled_object = base64.b64decode("{encoded_state}")
    current_contract = pickle.loads(decoded_pickled_object)
    
    contract_runner.mode = "{run_by}"
    
    if contract_runner.mode == "validator":
        contract_runner._load_leader_eq_outputs()

    if asyncio.iscoroutinefunction(current_contract.{function_name}):
        await current_contract.{function_name}({args_str})
    else:
        current_contract.{function_name}({args_str})

    pickled_object = pickle.dumps(current_contract)
    contract_runner._write_receipt(pickled_object, '{function_name}', [{args_str}])

if __name__=="__main__":
    import asyncio    
    asyncio.run(main())
    """


def get_nodes_config(logger=None) -> str:
    if logger:
        logger("Checking the nodes.json config file has been created...")
    cwd = os.path.abspath(os.getcwd())
    nodes_file = cwd + "/consensus/nodes/nodes.json"
    if not os.path.exists(nodes_file):
        raise Exception("Create a configuratrion file for the nodes")
    return json.load(open(nodes_file))


def genvm_url():
    return (
        os.environ["GENVMPROTOCOL"]
        + "://"
        + os.environ["GENVMHOST"]
        + ":"
        + os.environ["GENVMPORT"]
    )
