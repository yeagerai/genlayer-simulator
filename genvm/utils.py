import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


def debug_output(title: str, content: str):
    if int(os.environ.get("DEBUG")) == 1:
        print("--- START: " + title + " ---")
        print(f"""{content}""")
        print("--- END: " + title + " ---")


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

    debug_output("llm_config", node_config)

    with open(node_config_file, "w") as file:
        node_config["type"] = node_type
        json.dump(node_config, file, indent=4)
    file.close()

    debug_output("contract_code", contract_code)

    with open(contract_code_file, "w+") as file:
        file.write(contract_code)
    file.close()

    if leader_recipt:

        debug_output("Leader Recipt", leader_recipt)

        with open(leader_recipt_file, "w") as file:
            json.dump(leader_recipt, file, indent=4)
        file.close()


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
    contract_code: str,
    constructor_args: str,
    class_name: str,
) -> str:
    return f"""
{contract_code}

async def main():
    from genvm.base.contract_runner import ContractRunner
    contract_runner = ContractRunner()
    contract_runner._set_mode("leader")
    import pickle
    current_contract = {class_name}(**{constructor_args})
    
    pickled_object = pickle.dumps(current_contract)
    contract_runner._write_receipt(pickled_object, '__init__', [{constructor_args}])

if __name__=="__main__":
    import asyncio    
    asyncio.run(main())
    """


def generate_get_contract_data(
    contract_code: str,
    encoded_state: str,
    function_name: str,
    args_str: str,
) -> str:
    return f"""
{contract_code}

async def main():
    import pickle
    import base64
    decoded_pickled_object = base64.b64decode({encoded_state})
    current_contract = pickle.loads(decoded_pickled_object)
    return current_contract.{function_name}({args_str})

    
if __name__=="__main__":
    import asyncio    
    asyncio.run(main())
    """
