# GenLayer Prototype
## Introduction
Welcome to the GenLayer prototype, the first step towards a decentralized platform that combines the ease of using Python to write contracts, the access to the internet, the intelligence of the LLMs, and the security and efficiency of a blockchain.

## Prototype Components
The GenLayer prototype consists of the following main components:

* **State Storage (PostgreSQL):** We use a SQL database to maintain the blockchain's updated and persistent state.
* **State Manager (JSON-RPC Server):** A backend that processes requests, either to read the state of the blockchain or to execute transactions involving intelligent contracts.
* **Developer Interface:** CLI and some execution scripts to facilitate developers' interaction with the node, allowing the deployment and execution of intelligent contracts.
* **The Consensus Algorithm:** A python routine that launches execution processes into the GenVM, following the approach defined in the whitepaper.
* **Gen Virtual Machine (GenVM):** A Dockerized environment prepared to run intelligent contracts safely.

## Installation

### Window One

```
$ cp .env.example .env
$ docker compose build
$ docker compose up
```

### Window Two

#### 1. Installing the Ollama model

```
$ docker exec -it ollama ollama run llama2
...
```

#### 2. Set up the environment

##### Linux / MacOS
```
$ virtualenv .venv
$ source .venv/bin/activate
(.venv) $ pip install -r requirements.txt
(.venv) $ export PYTHONPATH="$(pwd)"
```

##### Windows (cmd)
```
$ virtualenv .venv
$  .\.venv\Scripts\activate
(.venv) $ pip install -r requirements.txt
(.venv) $ set PYTHONPATH=%cd%
```

##### Windows (PowerShell)
```
$ virtualenv .venv
$  .\.venv\Scripts\activate
(.venv) $ pip install -r requirements.txt
(.venv) $ $env:PYTHONPATH = (Get-Location).Path
```

#### Execute the Demo

```
(.venv) $ python scripts/debug_prototype.py
```

#### Seperate Steps

```
(.venv) $ python cli/genlayer.py create-db
...
(.venv) $ python cli/genlayer.py create-tables
...
(.venv) # python cli/genlayer.py create-account
{'id': 1, 'jsonrpc': '2.0', 'result': {'address': '0x...', 'balance': 0, 'status': 'account created'}}
(.venv) # python cli/genlayer.py fund-account --address 0x...
...
```


## Running the Nodes

1. Run `rpc/server.py` to start the server on port `4000`.

2. Set up the initial state:
   - Open a terminal and activate the virtual environment (if not already active):
     ```
     $ source .venv/bin/activate
     ```
   - Register validators:
     ```
     (.venv) # python cli/genlayer.py register-validators --count 10 --min-stake 1 --max-stake 10
     ```
     This command registers 10 validators with stakes ranging from 1.0 to 10.0.
   - Create an externally owned account (EOA):
     ```
     (.venv) # python cli/genlayer.py create-eoa --balance 10
     ```
     This command creates an EOA with a balance of 10.0. The output will include the account's ID, which you'll need in the next steps.
   - Deploy a contract:
     ```
     (.venv) # python cli/genlayer.py deploy --from-account <EOA_ID> genvm/contracts/wizzard_of_coin.py
     ```
     Replace `<EOA_ID>` with the ID of the EOA created in the previous step. This command deploys the "Wizzard of Coin" contract.
   - Interact with the deployed contract:
     ```
     (.venv) # python cli/genlayer.py contract --from-account <EOA_ID> --contract-address <CONTRACT_ADDRESS> --function WizzardOfCoin.ask_for_coin --args <EOA_ID> --args Dave
     ```
     Replace `<EOA_ID>` with the ID of the EOA and `<CONTRACT_ADDRESS>` with the address of the deployed contract from the previous step. This command calls the `ask_for_coin` function of the "Wizzard of Coin" contract.

   After executing these commands, you will have an initial state set up with validators, an EOA, and a deployed contract. You can check the changes in the DB using a viewer like `dbeaver`.

3. Execute transactions:
   - Use the `scripts/debug_contract.py` script to create and debug intelligent contracts.
   - Modify the script to define your own transactions and test them by executing the script.

Now you can create new intelligent contracts and test them by executing transactions with this prototype.
