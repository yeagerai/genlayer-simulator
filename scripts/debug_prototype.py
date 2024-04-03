import os
import sys
import time
from cli.genlayer import create_eoa_logic, register_validators_logic, count_validators_logic

print('Checking environement...')
# Check you in a viretualenv
if 'VIRTUAL_ENV' not in os.environ and 'CONDA_DEFAULT_ENV' not in os.environ:
    print('No active virtualenv or conda environment detected!')
    print('Please activate a virtualenv or a conda environment.')
    print('(If you don\'t know how to do this, please read the README.md or relevant documentation)')
    sys.exit()

# Make sure the file is being run from the project folder (not the scipts folder)
if os.path.basename(os.path.normpath(os.getcwd())) == 'scripts':
    print('Run this script from the project root')
    sys.exit()

# make sure the PYTHONPATH is set
# (export PYTHONPATH="/home/personal/Projects/Genlayer/genlayer-prototype")
if 'PYTHONPATH' not in os.environ:
    print('Run the following command:')
    print(('>>> export PYTHONPATH="'+os.getcwd()+'" <<<').format(42))
    sys.exit()


from cli.genlayer import (
    create_db_logic,
    create_tables_logic,
    last_contracts_logic,
    deploy_logic,
    contract_logic
)

# create the db and tables if you need to
print('Creating db and tables...')
create_db_logic()
create_tables_logic()

# create initial data
print('Creating validadtors and account...')
response = count_validators_logic()
if 'result' in response and 'count' in response['result']:
    if response['result']['count'] == 0:
        print('Creating validators...')
        register_validators_logic(10, 1, 10)
    else:
        print('Validators already created.')
else:
    raise Exception('The count_validators rpc function failed!')
create_account_result = create_eoa_logic(10)

new_account = None
if 'result' in create_account_result and 'id' in create_account_result['result']:
    new_account = create_account_result['result']['id']
else:
    raise Exception('Could not create new account!') 

# Your hardcoded values
contract_file_path = 'genvm/contracts/wizzard_of_coin.py'
function_to_execute = 'WizzardOfCoin.ask_for_coin'
initial_contract_state = '{"have_coin": true}'

# Wait a bit before starting
time.sleep(5)

# Deploy the contract
with open(contract_file_path, 'rb') as contract_file:
    deploy_output = deploy_logic(new_account, contract_file, initial_contract_state)
    print("Deploy command output:", deploy_output)

# Retrieve the last contract ID (you should parse the actual ID from the output)
last_contract_output = last_contracts_logic(1)
print("Last contract command output:", last_contract_output)
last_contract_id = last_contract_output['result'][0]['contract_id']  # Example parsing


# Call the contract
args = (new_account, "Can you please return me my coin?")
call_contract_output = contract_logic(new_account, last_contract_id, function_to_execute, args)
print("Call contract command output:", call_contract_output)
