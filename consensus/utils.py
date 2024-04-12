import os
import random
from database.credentials import get_genlayer_db_connection
import json


def vrf(items, weights, k):
    weighted_indices = random.choices(range(len(items)), weights=weights, k=k * 10)
    unique_indices = set()
    random.shuffle(weighted_indices)

    for idx in weighted_indices:
        unique_indices.add(idx)
        if len(unique_indices) == k:
            break

    return [items[i] for i in unique_indices]


def get_contract_state(contract_address: str) -> dict: # that should be on the rpc and cli maybe
    connection = get_genlayer_db_connection()
    cursor = connection.cursor()

    try:
        #TODO: This needs to be better
        cursor.execute(
            "SELECT data FROM current_state WHERE id = (%s);", (contract_address,)
        )
        contract_row = cursor.fetchone()
        if contract_row is not None:
            return contract_row[0]
        else:
            return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

def build_icontract(
        contract_code:str,
        contract_state:str,
        run_by:str,
        class_name:str,
        function_name:str,
        args_str:str
) -> str:
    return f"""
{contract_code}

async def main():
    current_contract = {class_name}(**{contract_state})
    current_contract.mode = "{run_by}"
    await current_contract.{function_name}({args_str})

if __name__=="__main__":
    import asyncio    
    asyncio.run(main())
    """

def get_nodes_config(logger=None) -> str:
    if logger:
        logger("Checking the nodes.json config file has been created...")
    cwd = os.path.abspath(os.getcwd())
    nodes_file = cwd + '/consensus/nodes/nodes.json'
    if not os.path.exists(nodes_file):
        raise Exception('Create a configuratrion file for the nodes')
    return json.load(open(nodes_file))


def get_validators(nodes_config:dict, logger=None) -> list:
    if logger:
        logger("Selecting validators with VRF...")
    # Select validators
    connection = get_genlayer_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT validator_info->>'eoa_id' AS validator_id, stake FROM validators;"
    )
    validator_data = cursor.fetchall()

    if len(nodes_config) < len(validator_data):
        raise Exception('Nodes in database ('+str(len(validator_data))+'). Nodes configured ('+str(len(nodes_config))+')')

    # Prepare validators and their stakes
    all_validators = [row[0] for row in validator_data]
    validators_stakes = [float(row[1]) for row in validator_data]

    return all_validators, validators_stakes

def genvm_url():
    return os.environ['GENVMPROTOCOL']+'://'+os.environ['GENVMHOST']+':'+os.environ['GENVMPORT']