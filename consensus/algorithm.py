import json
from database.credentials import get_genlayer_db_connection
from consensus.utils import vrf, get_contract_state, create_tar_archive, write_json_from_docker_tar
#import docker

#client = docker.from_env()

# Description: This will create the contract on the shared drive and then
#              call the genvm to execute it. This will later will be
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
    exec_file_name = "contract_execution.py"

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

    f = open('/icontracts/'+exec_file_name)
    f.write(exec_file_for_genvm)
    f.close()

    return leader_receipt

'''
    tar_stream = create_tar_archive(exec_file_name, exec_file_for_genvm)

    container = client.containers.create(image="genvm:latest", network_mode="host") # TODO: this has to be replaced with a compose and the ollama server there

    try:
        container.put_archive("/genvm/", tar_stream)

        container.start()

        logs = container.logs(stream=True)
        for line in logs:
            print(line.strip().decode())
            if "Leader execution has ended." in line.decode():
                bits, _ = container.get_archive("/genvm/receipt.json")
                print("Detected script completion.")
                break

        container.stop()

        write_json_from_docker_tar(bits, "genvm/receipt.json")

        with open("genvm/receipt.json", "r") as file:
            genvm_file = json.load(file)
        leader_receipt["contract_state"] = genvm_file["contract_state"]
        leader_receipt["non_det_inputs"] = genvm_file["non_det_inputs"]
        leader_receipt["non_det_outputs"] = genvm_file["non_det_outputs"]
    finally:
        container.remove()

    return leader_receipt
'''

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


async def exec_transaction(transaction_input):
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

    # Leader executes transaction
    leader_receipt = leader_executes_transaction(transaction_input, leader)
    votes = json.dumps({leader: leader_receipt["vote"]})


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
