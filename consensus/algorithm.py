import os
import json
import requests
from database.credentials import get_genlayer_db_connection
from database.types import ConsensusData
from consensus.utils import (
    vrf,
    get_contract_state,
    genvm_url,
    build_icontract,
    get_nodes_config,
    get_validators
)

from dotenv import load_dotenv
load_dotenv()

# Description: This will create the contract on the shared drive and then
#              call the genvm to execute it. This will be changed at a
#              later date
# TODO: deliver the contract through S3, postgres, celery or sent as part
#       of the call to the flaskapi in the genvm
def leader_executes_transaction(transaction_input:str, leader:str, leader_config:dict) -> dict:
    current_contract_state = get_contract_state(transaction_input["contract_address"])

    args_str = ", ".join(f"{json.dumps(arg)}" for arg in transaction_input["args"])

    class_name = transaction_input["function_name"].split('.')[0]
    function_name = transaction_input["function_name"].split('.')[1]

    exec_file_for_genvm = build_icontract(
        contract_code=current_contract_state['code'],
        contract_state=str(current_contract_state['state']),
        run_by='leader',
        class_name=class_name,
        function_name=function_name,
        args_str=args_str
    )

    payload = {
        "jsonrpc": "2.0",
        "method": "leader_executes_transaction",
        "params": [exec_file_for_genvm, leader_config],
        "id": 2,
    }
    
    response = requests.post(genvm_url()+'/api', json=payload).json()

    return {
        'class':class_name,
        'function':function_name,
        'vote': 'agree',
        'result': response['result']
    }


async def validator_executes_transaction(transaction_input, leader_receipt, validator):
    validator_receipt = {
        "validator":validator, 
        "contract_state":{}, 
        "eq_principles_outs":{}
    }

    # TODO: finish function

    if validator_receipt["contract_state"] == leader_receipt["contract_state"]:
        validator_receipt["vote"] = "agree"
    else:
        validator_receipt["vote"] = "disagree"
    return validator_receipt


async def exec_transaction(transaction_input, logger=None):

    nodes_config = get_nodes_config(logger)

    all_validators, validators_stakes = get_validators(nodes_config, logger)

    # Select validators using VRF
    selected_validators = vrf(all_validators, validators_stakes, 5)
    leader = selected_validators[0]
    remaining_validators = selected_validators[1:]
    if logger:
        logger(f"Selected Leader: {leader}...")
        logger(f"Selected Validators: {remaining_validators}...")
        logger(f"Leader {leader} starts contract execution...")

    leader_config = None
    for validator_config in nodes_config:
        if validator_config['id'] == leader:
            leader_config = validator_config

    if not leader_config:
        raise Exception('The config for node '+leader+' is not in consensus/nodes/nodes.json')
    
    # Leader executes transaction
    leader_result = leader_executes_transaction(transaction_input, leader, leader_config)

    votes = {leader: leader_result['vote']}

    if logger:
        logger(f"Leader {leader} has finished contract execution...")

    # Validators execute transaction
    # loop = asyncio.get_running_loop()
    # validation_tasks = [
    #     loop.create_task(validator_executes_transaction(transaction_input, leader_receipt, validator)) # watch out! as ollama uses GPU resources
    #     for validator in remaining_validators
    # ]
    # validation_results = await asyncio.gather(*validation_tasks)

    # for i in range(len(validation_results)):
    #     votes[f"{validation_results[i]['validator']}"] = validation_results[i]["vote"]

    # Write transaction into DB
    from_address = transaction_input['args'][0]
    to_address = transaction_input['contract_address']
    data = json.dumps({"new_contract_state" : leader_result['result']['contract_state']})
    transaction_type = 2
    final = False
    valudators_results = []
    consensus_data = ConsensusData(final=final, votes=votes, leader=leader_result, validators=valudators_results).model_dump_json()
    connection = get_genlayer_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO transactions (from_address, to_address, data, consensus_data, type, created_at) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP);",
        (
            from_address,
            to_address,
            data,
            consensus_data,
            transaction_type,
        ),
    )

    connection.commit()
    cursor.close()
    connection.close()

    if logger:
        logger(f"Transaction has been fully executed...")

    execution_output = {}
    execution_output["leader_data"] = leader_result
    execution_output["consensus_data"] = consensus_data
    return execution_output