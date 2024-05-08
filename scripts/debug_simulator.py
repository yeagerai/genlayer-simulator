import os
import sys
import time
import json

from dotenv import load_dotenv
load_dotenv()

cwd = os.path.abspath(os.getcwd())


# Make sure the file is being run from the project folder (not the scipts folder)
if not os.path.exists("scripts/debug_simulator.py"):
    print(cwd)
    print('Run this script from the project root')
    sys.exit()

# make sure the PYTHONPATH is set
# (export PYTHONPATH="/home/personal/Projects/Genlayer/genlayer-prototype")
if "PYTHONPATH" not in os.environ:
    print("Run the following command:")
    print(('$ export PYTHONPATH="'+os.getcwd()+'"').format(42))
    sys.exit()


from cli.genlayer import (
    create_random_validators_logic,
    count_validators_logic,
    create_db_logic,
    create_tables_logic,
    last_contracts_logic,
    deploy_logic,
    contract_logic,
    create_account_logic,
    fund_account_logic,
)

# create the db and tables if you need to
print('Creating db and tables...')
create_db_logic()
create_tables_logic()

# create initial data
print('Creating validadtors and account...')
response = count_validators_logic()
if 'result' in response and 'count' in response['result']['data']:
    if response['result']['data']['count'] == 0:
        print('Creating validators...')
        create_random_validators_logic(int(os.environ['TOTALVALIDATORS']), 1, 10)
    else:
        print('Validators already created.')
else:
    raise Exception('The count_validators rpc function failed!')

# Create a new account
create_account_result = create_account_logic()

new_account = None
if 'result' in create_account_result and 'address' in create_account_result['result']['data']:
    new_account = create_account_result['result']['data']['address']
    print('Account created! ('+new_account+')')
else:
    raise Exception('Could not create new account!') 

# Fund the new account
balance = 10
fund_account_result = fund_account_logic(new_account, balance)

if 'result' in fund_account_result and 'address' in fund_account_result['result']['data']:
    print('Account funded! ('+str(balance)+')')

# Your hardcoded values
contract_file_path = 'examples/contracts/wizzard_of_coin.py'
function_to_execute = 'WizzardOfCoin.ask_for_coin'
class_name = 'WizzardOfCoin'
initial_contract_state = '{"have_coin": "True"}'

# Deploy the contract
with open(contract_file_path, 'rb') as contract_file:
    deploy_output = deploy_logic(new_account, class_name, contract_file, initial_contract_state)
    print("Deploy command output:", deploy_output)

# Retrieve the last contract ID (you should parse the actual ID from the output)
last_contract_output = last_contracts_logic(1)
print("Last contract command output:", last_contract_output)
last_contract_id = last_contract_output['result']['data'][0]['address']  # Example parsing


# Call the contract
args = ["Can you please return me my coin?"]
call_contract_output = contract_logic(new_account, last_contract_id, function_to_execute, args)
print("Call contract command output:")
print(json.dumps(call_contract_output, indent=4))
