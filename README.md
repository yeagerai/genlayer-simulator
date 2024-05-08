# GenLayer Simulator

## Introduction

This Simulator is an interactive sandbox designed for developers to explore the potential of GenLayer's Intelligent Contracts. It replicates the GenLayer network's execution environment and consensus algorithm, but offers a controlled and local environment to test different ideas and behaviors.

## Simulator Components

The GenLayer simulator consists of the following main components:

* **State Storage (PostgreSQL):** We use a SQL database to maintain the blockchain's updated and persistent state.
* **State Manager (JSON-RPC Server):** A backend that processes requests, either to read the state of the blockchain or to execute transactions involving intelligent contracts.
* **Developer Interface:** CLI and some execution scripts to facilitate developers' interaction with the node, allowing the deployment and execution of intelligent contracts.
* **The Consensus Algorithm:** A python routine that launches execution processes into the GenVM, following the approach defined in the whitepaper.
* **Gen Virtual Machine (GenVM):** A Dockerized environment prepared to run intelligent contracts safely.

## Quick Install

```
$ npm install -g genlayer
$ genlayer init
```

To run genlayer again just run:

```
$ genlayer up
```

*(Additional installation instructions can be found [here](https://docs.genlayer.com/simulator/installation))*

Then visit [localhost:8080](http://localhost:8080/)

From here you will be able to create validators and intellegent contracts.

## Installing Manually

### Window One

```
$ cp .env.example .env
$ docker compose up
```

### Window Two

#### 1. Installing the Ollama model

```
$ docker exec -it ollama ollama run llama3
...
```

#### 2. Setup your environment

Setup your environment [here](#set-up-an-environment)

#### 3. Execute the Demo

```
(.venv) $ python scripts/debug_simulator.py
```

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

<a name="set-up-an-environment"></a>
## Set up an environment

### Linux / MacOS
```
$ virtualenv .venv
$ source .venv/bin/activate
(.venv) $ pip install -r requirements.txt
(.venv) $ export PYTHONPATH="$(pwd)"
```

### Windows (cmd)
```
$ virtualenv .venv
$  .\.venv\Scripts\activate
(.venv) $ pip install -r requirements.txt
(.venv) $ set PYTHONPATH=%cd%
```

### Windows (PowerShell)
```
$ virtualenv .venv
$  .\.venv\Scripts\activate
(.venv) $ pip install -r requirements.txt
(.venv) $ $env:PYTHONPATH = (Get-Location).Path
```

## Documentation

Additional documentation

 - https://docs.genlayer.com/