import time
from cli.genlayer import (
    last_contracts_logic,
    deploy_logic,
    contract_logic,
)

# Your hardcoded values
hardcoded_from_address = '95594942-17e5-4f91-8862-c3a4eae5b58c'
contract_file_path = 'genvm/contracts/wizzard_of_coin.py'
function_to_execute = 'WizzardOfCoin.ask_for_coin'
initial_contract_state = '{"have_coin": true}'

# Wait a bit before starting
time.sleep(5)

# Deploy the contract
with open(contract_file_path, 'rb') as contract_file:
    deploy_output = deploy_logic(hardcoded_from_address, contract_file, initial_contract_state)
    print("Deploy command output:", deploy_output)

# Retrieve the last contract ID (you should parse the actual ID from the output)
last_contract_output = last_contracts_logic(1)
print("Last contract command output:", last_contract_output)
last_contract_id = last_contract_output['result'][0]['contract_id']  # Example parsing

# Call the contract
args = (hardcoded_from_address, "Can you please return me my coin?")
call_contract_output = contract_logic(hardcoded_from_address, last_contract_id, function_to_execute, args)
print("Call contract command output:", call_contract_output)