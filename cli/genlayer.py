import json
import click
import requests
import random
from os import environ
from typing import IO

from dotenv import load_dotenv
load_dotenv()

json_rpc_url = environ.get('RPCPROTOCOL')+"://localhost:"+environ.get('RPCPORT')+"/api"


def create_db_logic() -> dict:
    payload = {
        "jsonrpc": "2.0",
        "method": "create_db",
        "params": [],
        "id": 1,
    }
    response = requests.post(json_rpc_url, json=payload).json()
    return response

def create_tables_logic() -> dict:
    payload = {
        "jsonrpc": "2.0",
        "method": "create_tables",
        "params": [],
        "id": 1,
    }
    response = requests.post(json_rpc_url, json=payload).json()
    return response

def create_account_logic() -> dict:
    payload = {
        "jsonrpc": "2.0",
        "method": "create_account",
        "params": [],
        "id": 1,
    }
    response = requests.post(json_rpc_url, json=payload).json()
    return response

def fund_account_logic(address:str, balance:float) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "method": "fund_account",
        "params": [address, balance],
        "id": 1,
    }
    response = requests.post(json_rpc_url, json=payload).json()
    return response

def send_logic(from_account:str, to_account:str, amount:float) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "method": "send_transaction",
        "params": [from_account, to_account, amount],
        "id": 0,
    }
    response = requests.post(json_rpc_url, json=payload).json()
    return response

def deploy_logic(from_account:str, contract_code_file:IO[bytes], initial_state:str) -> dict:
    contract_code = contract_code_file.read()
    
    try:
        initial_state_dict = json.loads(initial_state)
    except json.JSONDecodeError as e:
        click.echo(f"Error parsing initial state JSON: {e}")
        return

    payload = {
        "jsonrpc": "2.0",
        "method": "deploy_intelligent_contract",
        "params": [from_account, contract_code.decode("utf-8"), initial_state_dict],
        "id": 2,
    }
    response = requests.post(json_rpc_url, json=payload).json()
    return response

def contract_logic(from_account:str, contract_address:str, function:str, args:tuple) -> dict:
    args_list = list(args)
    payload = {
        "jsonrpc": "2.0",
        "method": "call_contract_function",
        "params": [from_account, contract_address, function, args_list],
        "id": 3,
    }
    response = requests.post(json_rpc_url, json=payload).json()
    return response

def count_validators_logic() -> list:
    payload = {
        "jsonrpc": "2.0",
        "method": "count_validators",
        "params": [],
        "id": 4,
    }
    return requests.post(json_rpc_url, json=payload).json()

def register_validators_logic(count:int, min_stake:float, max_stake:float) -> list:
    responses = []
    for _ in range(count):
        stake = random.uniform(min_stake, max_stake)

        payload = {
            "jsonrpc": "2.0",
            "method": "register_validator",
            "params": [stake],
            "id": 4,
        }
        responses.append(requests.post(json_rpc_url, json=payload).json())
    return responses

def last_contracts_logic(number:int) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "method": "get_last_contracts",  # Assuming this is the correct method name on your JSON RPC server
        "params": [number],
        "id": 5, 
    }
    response = requests.post(json_rpc_url, json=payload).json()
    return response


# -- Click Commands ---


@click.group()
def cli():
    pass


@click.command(
    help="Create the GenLayer database"
)
def create_db():
    response = create_db_logic()
    click.echo(response)

@click.command(
    help="Create the GenLayer tables"
)
def create_tables():
    response = create_tables_logic()
    click.echo(response)

@click.command(
    help="Create a new account"
)
def create_account():
    response = create_account_logic()
    click.echo(response)

@click.command(
    help="Add funds to an account"
)
@click.option(
    "--address", type=str, required=True, help="The address you would like to add the funds to."
)
@click.option(
    "--balance", type=float, default=10, help="Funds to add to account."
)
def fund_account(address, balance):
    response = fund_account_logic(address, balance)
    click.echo(response)

@click.command(help="Send currency from one account to another.")
@click.option("--from-account", required=True, help="The sender's account address.")
@click.option("--to-account", required=True, help="The recipient's account address.")
@click.option("--amount", type=float, required=True, help="The amount to send.")
def send(from_account, to_account, amount):
    response = send_logic(from_account, to_account, amount)
    click.echo(response)


@click.command(help="Deploy a new intelligent contract.")
@click.option(
    "--from-account",
    required=True,
    help="The account from which the contract will be deployed.",
)
@click.option(
    "--initial-state",
    required=True,
    default="{}",
    help="Initial state of the contract as a JSON string.",
)
@click.argument("contract_code_file", type=click.File("rb"))
def deploy(from_account, contract_code_file, initial_state):
    response = deploy_logic(from_account, contract_code_file, initial_state)
    click.echo(response)
    return response


@click.command(help="Interact with a deployed contract.")
@click.option(
    "--from-account", required=True, help="The account from which the call is made."
)
@click.option(
    "--contract-address",
    required=True,
    help="The address of the contract to interact with.",
)
@click.option("--function", required=True, help="The contract function to call.")
@click.option(
    "--args", multiple=True, type=str, help="Arguments for the function call."
)
def contract(from_account, contract_address, function, args):
    response = contract_logic(from_account, contract_address, function, args)
    click.echo(response)

@click.command(help="Tells you how many validators there are in the network.")
def count_validators(count, min_stake, max_stake):
    response = count_validators_logic()
    click.echo(
        f"There are {response['count']} validators in the network."
    )


@click.command(help="Register X validators to the network with random stakes.")
@click.option(
    "--count", type=int, required=True, help="Number of validators to register."
)
@click.option(
    "--min-stake", type=float, required=True, help="Minimum stake for each validator."
)
@click.option(
    "--max-stake", type=float, required=True, help="Maximum stake for each validator."
)
def register_validators(count, min_stake, max_stake):
    responses = register_validators_logic(count, min_stake, max_stake)
    click.echo(
        f"Registered {len(responses)} validators with stakes ranging from {min_stake} to {max_stake}."
    )

@click.command(help="Retrieve the last N deployed contracts.")
@click.option(
    "--number", type=int, required=True, help="Number of last deployed contracts to retrieve."
)
def last_contracts(number):
    response = last_contracts_logic(number)
    click.echo(json.dumps(response))
    return response

# setup commands
cli.add_command(create_db)
cli.add_command(create_tables)

## read commands
cli.add_command(last_contracts)

## write commands
cli.add_command(create_account)
cli.add_command(fund_account)
cli.add_command(register_validators)
cli.add_command(send)

cli.add_command(deploy)
cli.add_command(contract)

if __name__ == "__main__":
    cli()
