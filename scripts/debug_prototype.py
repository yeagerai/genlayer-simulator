import os
import sys
import time

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
# (export PYTHONPATH="${PYTHONPATH}:/home/personal/Projects/Genlayer/genlayer-prototype")
if 'PYTHONPATH' not in os.environ:
    print('Run the following command:')
    print(('>>> export PYTHONPATH="${{PYTHONPATH}}:'+os.getcwd()+'" <<<').format(42))
    sys.exit()


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

import sys
sys.exit()

# Retrieve the last contract ID (you should parse the actual ID from the output)
last_contract_output = last_contracts_logic(1)
print("Last contract command output:", last_contract_output)
last_contract_id = last_contract_output['result'][0]['contract_id']  # Example parsing

# Call the contract
args = (hardcoded_from_address, "Can you please return me my coin?")
call_contract_output = contract_logic(hardcoded_from_address, last_contract_id, function_to_execute, args)
print("Call contract command output:", call_contract_output)