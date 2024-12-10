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

        # Accounts
        accounts = self.get_accounts()
        self.owner = accounts["owner"]
        self.validator1 = accounts["validator1"]
        self.validator2 = accounts["validator2"]
        self.validator3 = accounts["validator3"]

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
                Path("/app/hardhat/deployments/hardhat") / f"{contract_name}.json"
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

    def _send_transaction(self, contract_function):
        """
        Helper method to send transactions

        Args:
            contract_function (ContractFunction): The contract function to send

        Returns:
            Optional[dict]: The transaction receipt or None if the transaction fails
        """
        try:
            # Build the transaction
            transaction = contract_function.build_transaction(
                {
                    "from": self.owner,
                    "nonce": self.web3.eth.get_transaction_count(self.owner),
                    "gas": 500000,  # Adjust gas as needed
                    "gasPrice": self.web3.eth.gas_price,
                }
            )

            # Send the transaction
            signed_tx = self.web3.eth.account.sign_transaction(
                transaction, private_key=self.private_key
            )
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)

            # Wait for the transaction to be mined
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return receipt
        except Exception as e:
            print(f"CONSENSUS_SERVICE: Transaction failed: {str(e)}")
            return None

    def get_accounts(self):
        """
        Get the available accounts from the network

        Returns:
            dict: A dictionary with the available accounts
        """
        accounts = self.web3.eth.accounts
        return {
            "owner": accounts[0],
            "validator1": accounts[1],
            "validator2": accounts[2],
            "validator3": accounts[3],
        }

    def deploy_fixture(self):
        """
        Deploy and initialize all contracts with proper connections
        """
        try:
            accounts = self.get_accounts()

            # Initialize GhostFactory
            if self.ghost_factory_contract:
                print("CONSENSUS_SERVICE: Setting up GhostFactory...")
                self._send_transaction(
                    self.ghost_factory_contract.functions.initialize()
                )
                self._send_transaction(
                    self.ghost_factory_contract.functions.setGhostBlueprint(
                        self.ghost_blueprint_contract.address
                    )
                )
                self._send_transaction(
                    self.ghost_factory_contract.functions.deployNewBeaconProxy()
                )

            # Initialize ConsensusMain
            if self.consensus_main_contract:
                print("CONSENSUS_SERVICE: Setting up ConsensusMain...")
                self.consensus_manager_address = self.consensus_manager_contract.address
                self.consensus_main_owner = (
                    self.consensus_main_contract.functions.owner()
                )
                self._send_transaction(
                    self.consensus_main_contract.functions.initialize(
                        self.consensus_manager_address
                    )
                )

                # Set up all contract connections
                if self.transactions_contract:
                    self._send_transaction(
                        self.transactions_contract.functions.initialize(
                            self.consensus_main_contract.address
                        )
                    )

                if self.queues_contract:
                    self._send_transaction(
                        self.queues_contract.functions.initialize(
                            self.consensus_main_contract.address
                        )
                    )

                self._send_transaction(
                    self.consensus_main_contract.functions.setGhostFactory(
                        self.ghost_factory_contract.address
                    )
                )
                self._send_transaction(
                    self.consensus_main_contract.functions.setGenStaking(
                        self.mock_gen_staking_contract.address
                    )
                )
                self._send_transaction(
                    self.consensus_main_contract.functions.setGenQueue(
                        self.queues_contract.address
                    )
                )
                self._send_transaction(
                    self.consensus_main_contract.functions.setGenTransactions(
                        self.transactions_contract.address
                    )
                )

            # Initialize other contracts and set their connections
            if self.ghost_factory_contract and self.consensus_main_contract:
                self._send_transaction(
                    self.ghost_factory_contract.functions.setGenConsensus(
                        self.consensus_main_contract.address
                    )
                )
                self._send_transaction(
                    self.ghost_factory_contract.functions.setGhostManager(
                        self.consensus_main_contract.address
                    )
                )

            if self.transactions_contract and self.consensus_main_contract:
                self._send_transaction(
                    self.transactions_contract.functions.setGenConsensus(
                        self.consensus_main_contract.address
                    )
                )

            if self.consensus_main_contract:
                self._send_transaction(
                    self.consensus_main_contract.functions.setAcceptanceTimeout(0)
                )

            # Setup validators
            if self.mock_gen_staking_contract:
                print("CONSENSUS_SERVICE: Setting up validators...")
                self._send_transaction(
                    self.mock_gen_staking_contract.functions.addValidators(
                        [
                            accounts["validator1"],
                            accounts["validator2"],
                            accounts["validator3"],
                        ]
                    )
                )

        except Exception as e:
            print(f"CONSENSUS_SERVICE: Error deploying fixture: {e}")
            return None
