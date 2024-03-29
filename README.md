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

```
$ sudo apt install postgresql
$ sudo -u postgres psql
# ALTER USER postgres WITH PASSWORD 'postgres';
# ALTER USER postgres WITH SUPERUSER;
# flush
# \q
$ sudo apt-get install libpq-dev
$ sudo apt-get install python3-psycopg2
$ virtualenv .venv
$ source .venv/bin/activate
(.venv) $ pip install -r rewquirments.txt
(.venv) $ export PYTHONPATH="${PYTHONPATH}:/.../genlayer-prototype"
(.venv) $ python python cli/genlayer.py create-db
(.venv) $ python python cli/genlayer.py create-tables
```

* Install `postgresql` on your computer and start the server.
* Create a user in the `postgresql` server named `postgresql` with password `postgresql`.
* Create a new venv called `genlayer` with `python 3.11`. For instance `conda create --name genlayer python=3.11`.
* Activate venv and install requirements.
* Execute `python database/init_db.py` to create the tables of the db.
* Build GenVM docker image. First `cd` into `genvm` folder. Then `docker build -t genvm .`.

## Execution

* Run `rpc/server.py` to launch the server on port `4000`.
* Run some CLI commands to create an initial state with validators, and deployed contracts:
    ```
    python genlayer.py register-validators --count 10 --min-stake 1 --max-stake 10

    New validator registered with stake 1.51
    New validator registered with stake 6.96
    New validator registered with stake 7.40
    New validator registered with stake 3.95
    New validator registered with stake 7.30
    New validator registered with stake 2.26
    New validator registered with stake 4.34
    New validator registered with stake 8.26
    New validator registered with stake 9.87
    New validator registered with stake 8.13
    Registered 10 validators with stakes ranging from 1.0 to 10.0.
    ```
    ```
    python genlayer.py create-eoa --balance 10
    
    {'id': 1, 'jsonrpc': '2.0', 'result': {'balance': 10.0, 'id': '95594942-17e5-4f91-8862-c3a4eae5b58c', 'status': 'EOA created'}}
    ```
    ```
    python genlayer.py deploy --from-account 95594942-17e5-4f91-8862-c3a4eae5b58c /home/user/Documents/genlayer/genlayer-node-prototype/contracts/wizzard_of_coin.py
    
    {{'30a079b5-4615-4b4f-a7c8-807f1f9d1577', 'status': 'deployed'}}
    ```

    That will create an initial state that enables the user to start sending transactions to the network. You can check all the changes on DB with a viewer such as `dbeaver`.

* Execute a transaction. You can use the `scripts/debug_contract.py` there you would see the execution syntax, and you can start creating and debugging intelligent contracts.

From now on you can create new intelligent contracts and test them by executing transactions with this prototype.
