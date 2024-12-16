import json
import os
from web3 import Web3
from eth_account import Account
from typing import Optional
from pathlib import Path


class ConsensusService:
    def __init__(self):
        """
        Initialize the ConsensusService class
        """
        # Connect to Hardhat Network
        port = os.environ.get("HARDHAT_PORT")
        url = os.environ.get("HARDHAT_URL")
        hardhat_url = f"{url}:{port}"
        self.web3 = Web3(Web3.HTTPProvider(hardhat_url))

        if not self.web3.is_connected():
            raise ConnectionError(f"Failed to connect to Hardhat node at {hardhat_url}")

        # Set up the default account (similar to ethers.getSigners()[0])
        self.owner = self.web3.eth.accounts[0]
        self.web3.eth.default_account = self.owner
        self.private_key = os.environ.get("HARDHAT_PRIVATE_KEY")

        # Load all required contracts
        self.ghost_contract = self._load_contract("GhostContract")
        self.ghost_factory_contract = self._load_contract("GhostFactory")
        self.ghost_blueprint_contract = self._load_contract("GhostBlueprint")
        self.consensus_manager_contract = self._load_contract("ConsensusManager")
        self.mock_gen_staking_contract = self._load_contract("MockGenStaking")
        self.queues_contract = self._load_contract("Queues")
        self.transactions_contract = self._load_contract("Transactions")
        self.consensus_main_contract = self._load_contract("ConsensusMain")

    def _load_contract(self, contract_name: str) -> Optional[dict]:
        """
        Load contract deployment data from Hardhat deployments

        Args:
            contract_name (str): The name of the contract to load

        Returns:
            Optional[dict]: The contract deployment data or None if loading fails
        """
        try:
            # Path to deployment file (using Docker volume path)
            deployment_path = (
                Path("/app/hardhat/deployments/localhost") / f"{contract_name}.json"
            )

            if not deployment_path.exists():
                print(
                    f"CONSENSUS_SERVICE: Deployment file not found at {deployment_path}"
                )
                return None

            with open(deployment_path, "r") as f:
                deployment_data = json.load(f)

            # Create contract instance
            contract = self.web3.eth.contract(
                address=deployment_data["address"], abi=deployment_data["abi"]
            )
            print(
                f"CONSENSUS_SERVICE: Loaded {contract_name} contract with address {contract.address}"
            )

            return contract

        except FileNotFoundError:
            print(
                f"CONSENSUS_SERVICE: Warning: {contract_name} deployment file not found"
            )
            return None
        except json.JSONDecodeError as e:
            print(
                f"CONSENSUS_SERVICE: Error decoding {contract_name} deployment file: {str(e)}"
            )
            return None
        except Exception as e:
            print(
                f"CONSENSUS_SERVICE: Error loading {contract_name} contract: {str(e)}"
            )
            return None