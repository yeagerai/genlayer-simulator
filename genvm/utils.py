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
    recipt_file = file_path + "/receipt.json"
    node_config_file = file_path + "/node-config.json"
    leader_recipt_file = file_path + "/leader-recipt.json"

    return icontract_file, recipt_file, node_config_file, leader_recipt_file


def save_files(
    icontract: str, node_config: str, node_type: str, leader_recipt: str = None
):
    icontract_file, _, node_config_file, leader_recipt_file = transaction_files()

    debug_output("llm_config", node_config)

    with open(node_config_file, "w") as file:
        node_config["type"] = node_type
        json.dump(node_config, file, indent=4)
    file.close()

    debug_output("icontract", icontract)

    with open(icontract_file, "w+") as file:
        file.write(icontract)
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
