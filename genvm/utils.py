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
