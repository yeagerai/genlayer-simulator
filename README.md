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

### Window One - Set up the Docker environment

```
$ cp .env.example .env
$ vim .env
GENVMOPENAIKEY     = '...' # Replace the placeholder with your actual OpenAI API key
$ docker-compose build
$ docker-compose up
```

### Window Two

#### 1. Install the Ollama model

```
$ docker exec -it ollama ollama run llama2
```

#### 2. Set up the virtual environment

  ```
  $ virtualenv .venv
  $ source .venv/bin/activate
  (.venv) $ pip install -r requirements.txt
  (.venv) $ export PYTHONPATH="$(pwd)"
  ```

For Windows users, see the instructions at the bottom of this [README](#instructions-for-windows-users).

#### 3. Execute the demo

Run the demo script to create an initial state with validators, deploy a sample contract, and execute a transaction on the contract.

```
(.venv) $ python scripts/debug_prototype.py
```

#### Alternative: Execute the steps separately

If you prefer to run the steps separately instead of using the demo script, follow these commands:

1. Create the database:
   ```
   (.venv) $ python cli/genlayer.py create-db
   ```
2. Create the tables:
   ```
   (.venv) $ python cli/genlayer.py create-tables
   ```
3. Create an account:
   ```
   (.venv) # python cli/genlayer.py create-account
   {'id': 1, 'jsonrpc': '2.0', 'result': {'address': '0xE36Ecf4fAc0EC678dbc0FD33280ff6A99C974e8d', 'balance': 0, 'status': 'account created'}}
   ``` 
4. Fund the account:
   ```
   (.venv) # python cli/genlayer.py fund-account --address 0xE36Ecf4fAc0EC678dbc0FD33280ff6A99C974e8d
   ```  
5. Register validators:
   ```
   (.venv) # python cli/genlayer.py register-validators --count 10 --min-stake 1 --max-stake 10
   Registered 10 validators with stakes ranging from 1.0 to 10.0.
   ``` 
6. Deploy a contract:
    ```
   (.venv) # python cli/genlayer.py deploy --from-account 0xE36Ecf4fAc0EC678dbc0FD33280ff6A99C974e8d genvm/contracts/wizzard_of_coin.py
   {'id': 2, 'jsonrpc': '2.0', 'result': {'contract_id': '0xFdCAf400cC808EfcBAfD1f6Ff53beEbfFea4bcEb', 'status': 'deployed'}}
   ```
7. Interact with the deployed contract:
   ```
   (.venv) # python cli/genlayer.py contract --from-account 0xE36Ecf4fAc0EC678dbc0FD33280ff6A99C974e8d --contract-address 0xFdCAf400cC808EfcBAfD1f6Ff53beEbfFea4bcEb --function WizzardOfCoin.ask_for_coin --args 0xFdCAf400cC808EfcBAfD1f6Ff53beEbfFea4bcEb --args Dave
   {'id': 3, 'jsonrpc': '2.0', 'result': {'message': "Function 'WizzardOfCoin.ask_for_coin' called on contract at 0xFdCAf400cC808EfcBAfD1f6Ff53beEbfFea4bcEb with args ['0xFdCAf400cC808EfcBAfD1f6Ff53beEbfFea4bcEb', 'Dave'].", 'status': 'success'}}
   ```
🧨 **Note:** Replace `0xE36Ecf4fAc0EC678dbc0FD33280ff6A99C974e8d` with account address and `0xFdCAf400cC808EfcBAfD1f6Ff53beEbfFea4bcEb` with your own contract_id.
  
You can check the changes in the database using a viewer like `dbeaver`.

## Instructions for Windows Users

If you are using Windows, follow these steps to set up the virtual environment:

- For Windows (cmd):
  ```
  $ virtualenv .venv
  $ .\\.venv\\Scripts\\activate
  (.venv) $ pip install -r requirements.txt
  (.venv) $ set PYTHONPATH=%cd%
  ```
- For Windows (PowerShell):
  ```
  $ virtualenv .venv
  $ .\\.venv\\Scripts\\activate
  (.venv) $ pip install -r requirements.txt
  (.venv) $ $env:PYTHONPATH = (Get-Location).Path
  ```
After setting up the virtual environment, you can continue with the installation process as described above.
