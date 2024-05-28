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
