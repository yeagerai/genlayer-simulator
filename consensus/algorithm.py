import json
import requests
from database.credentials import get_genlayer_db_connection
from consensus.utils import vrf, get_contract_state, genvm_url

from dotenv import load_dotenv
load_dotenv()

# Description: This will create the contract on the shared drive and then
#              call the genvm to execute it. This will be changed at a
#              later date
# TODO: deliver the contract through S3, postgres, celery or sent as part
#       of the call to the flaskapi in the genvm
def leader_executes_transaction(transaction_input, leader):
    leader_receipt = {
        "leader":leader, 
        "contract_state":{}, 
        "non_det_inputs": {}, 
        "non_det_outputs":{},
        "vote":"agree"
    }
    current_contract_state = get_contract_state(transaction_input["contract_address"])

    args_str = ", ".join(f"{json.dumps(arg)}" for arg in transaction_input["args"])

    exec_file_for_genvm = f"""
{current_contract_state['code']}

async def main():
    current_contract = {transaction_input["function"].split('.')[0]}(**{str(current_contract_state['state'])})
    current_contract.mode = "leader"
    await current_contract.{transaction_input["function"].split('.')[1]}({args_str})

if __name__=="__main__":
    import asyncio    
    asyncio.run(main())
    """

    payload = {
        "jsonrpc": "2.0",
        "method": "leader_executes_transaction",
        "params": [exec_file_for_genvm],
        "id": 2,
    }
    result = requests.post(genvm_url()+'/api', json=payload).json()

    if 'result' in result and 'status' in result['result']:
        leader_receipt["contract_state"] = result["result"]["status"]["contract_state"]
        leader_receipt["non_det_inputs"] = result["result"]["status"]["non_det_inputs"]
        leader_receipt["non_det_outputs"] = result["result"]["status"]["non_det_outputs"]
    else:
        raise Exception("The GenVM responded with: "+str(result))

    return leader_receipt


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
    if logger:
        logger("Selecting validators with VRF...")
    # Select validators
    connection = get_genlayer_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT validator_info->>'eoa_id' AS validator_id, stake FROM validators;"
    )
    validator_data = cursor.fetchall()

    # Prepare validators and their stakes
    all_validators = [row[0] for row in validator_data]
    validators_stakes = [float(row[1]) for row in validator_data]

    # Select validators using VRF
    selected_validators = vrf(all_validators, validators_stakes, 5)
    leader = selected_validators[0]
    remaining_validators = selected_validators[1:]
    if logger:
        logger(f"Selected Leader: {leader}...")
        logger(f"Selected Validators: {remaining_validators}...")
        logger(f"Leader {leader} starts contract execution...")
    # Leader executes transaction
    leader_receipt = leader_executes_transaction(transaction_input, leader)
    votes = json.dumps({leader: leader_receipt["vote"]})

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
    from_address = transaction_input["args"][0]
    to_address = transaction_input["contract_address"]
    data = json.dumps({"new_contract_state" : leader_receipt["contract_state"]})
    transaction_type = 2
    final = False
    leader_data = json.dumps(leader_receipt)

    cursor.execute(
        "INSERT INTO transactions (from_address, to_address, data, type, created_at, final, votes, leader_data) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s);",
        (
            from_address,
            to_address,
            data,
            transaction_type,
            final,
            votes,
            leader_data,
        ),
    )

    connection.commit()
    cursor.close()
    connection.close()

    if logger:
        logger(f"Transaction has been fully executed...")
