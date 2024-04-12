import time
from click.testing import CliRunner
from cli.genlayer import cli

# Hardcoded values (change after install)
hardcoded_from_address = '95594942-17e5-4f91-8862-c3a4eae5b58c'
contract_file_path = 'genvm/contracts/wizzard_of_coin.py' 
function_to_execute = 'WizzardOfCoin.ask_for_coin'
initial_contract_state = '{"have_coin": true}'

runner = CliRunner()

# Invoke the deploy command
with open(contract_file_path, 'rb') as contract_file:
    deploy_output = runner.invoke(cli, ['deploy', '--from-account', hardcoded_from_address, '--initial-state', initial_contract_state, contract_file])
    print("Deploy command output:", deploy_output.output)

# Invoke the last_contracts command
last_contract_output = runner.invoke(cli, ['last-contracts', '--number', '1'])
print("Last contract command output:", last_contract_output.output)
last_contract_id = last_contract_output.output['result'][0]['contract_id']

# Invoke the contract command
call_contract_output = runner.invoke(cli, ['contract', '--from-account', hardcoded_from_address, '--contract-address', last_contract_id, '--function', function_to_execute, '--args', hardcoded_from_address, '--args', "Can you please return me my coin?"])
print("Call contract command output:", call_contract_output.output)
