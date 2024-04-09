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

## Nodes

* Run `rpc/server.py` to launch the server on port `4000`.
* Run some CLI commands to create an initial state with validators, and deployed contracts:
    ```
    (.venv) # python cli/genlayer.py register-validators --count 10 --min-stake 1 --max-stake 10
    Registered 10 validators with stakes ranging from 1.0 to 10.0.
    (.venv) # python cli/genlayer.py create-eoa --balance 10
    {'id': 1, 'jsonrpc': '2.0', 'result': {'balance': 10.0, 'id': '95594942-17e5-4f91-8862-c3a4eae5b58c', 'status': 'EOA created'}}
    (.venv) # python cli/genlayer.py deploy --from-account 95594942-17e5-4f91-8862-c3a4eae5b58c genvm/contracts/wizzard_of_coin.py
    {{'30a079b5-4615-4b4f-a7c8-807f1f9d1577', 'status': 'deployed'}}
    (.venv) # python cli/genlayer.py contract --from-account <from_address> --contract-address 30a079b5-4615-4b4f-a7c8-807f1f9d1577 --function WizzardOfCoin.ask_for_coin --args <from_address> --args Dave
    {'id': 3, 'jsonrpc': '2.0', 'result': {'message': "Function 'WizzardOfCoin.ask_for_coin' called on contract at 30a079b5-4615-4b4f-a7c8-807f1f9d1577 with args ['<from_address>', 'Dave'].", 'status': 'success'}}
    ```

    *(NOTE: <from_address> can be '95594942-17e5-4f91-8862-c3a4eae5b58c' or another address)*

    That will create an initial state that enables the user to start sending transactions to the network. You can check all the changes on DB with a viewer such as `dbeaver`.

* Execute a transaction. You can use the `scripts/debug_contract.py` there you would see the execution syntax, and you can start creating and debugging intelligent contracts.

From now on you can create new intelligent contracts and test them by executing transactions with this prototype.
