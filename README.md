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
$ npm install -g genlayer
$ genlayer init
```

Then visit [localhost:8080](http://localhost:8080/)

From here you will be able to create validators and intellegent contracts.

## CLI commands

Use the following commands to run through a demo step-by-step.

```
(.venv) $ python cli/genlayer.py create-db
...
(.venv) $ python cli/genlayer.py create-tables
...
(.venv) # python cli/genlayer.py create-random-validators --count 10 --min-stake 1 --max-stake 10
...
(.venv) # python cli/genlayer.py create-eoa --balance 10
...<your-new-address>...
(.venv) # python cli/genlayer.py deploy --from-account <your-new-address> --initial-state {"have_coin": True} examples/contracts/wizzard_of_coin.py
...<contract-address>...
(.venv) # python cli/genlayer.py contract --from-account <your-new-address> --contract-address <contract-address> --function WizzardOfCoin.ask_for_coin --args {"request": "Can I have the coin please?"}
...
```

*(NOTE: You can find the full list of CLI commands [here](https://github.com/yeagerai/genlayer-simulator/blob/main/cli/genlayer.py))*

## Documentation

Additional documentation

 - https://genlayer-docs.netlify.app/