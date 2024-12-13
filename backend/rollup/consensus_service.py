import json
import os
from web3 import Web3
from typing import Optional
from pathlib import Path
from backend.protocol_rpc.message_handler.base import MessageHandler
from backend.protocol_rpc.message_handler.types import EventType, EventScope, LogEvent


class ConsensusService:
    def __init__(self, msg_handler: MessageHandler):
        """
        Initialize the ConsensusService class
        """
        # Connect to Hardhat Network
        port = os.environ.get("HARDHAT_PORT")
        url = os.environ.get("HARDHAT_URL")
        hardhat_url = f"{url}:{port}"
        self.web3 = Web3(Web3.HTTPProvider(hardhat_url))

        self.msg_handler = msg_handler

        if not self.web3.is_connected():
            raise ConnectionError(f"Failed to connect to Hardhat node at {hardhat_url}")

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
                self.msg_handler.send_message(
                    LogEvent(
                        "consensus_service_call",
                        EventType.ERROR,
                        EventScope.CONSENSUS,
                        f"CONSENSUS_SERVICE: Deployment file not found at {deployment_path}",
                        {
                            "function_name": "_load_contract",
                            "contract_name": contract_name,
                        },
                    )
                )
                return None

            with open(deployment_path, "r") as f:
                deployment_data = json.load(f)

            self.msg_handler.send_message(
                LogEvent(
                    "consensus_service_call",
                    EventType.INFO,
                    EventScope.CONSENSUS,
                    f"CONSENSUS_SERVICE: Loaded {contract_name} contract with address {deployment_data['address']}",
                    {"function_name": "_load_contract", "contract_name": contract_name},
                )
            )

            return {
                "address": deployment_data["address"],
                "abi": deployment_data["abi"],
            }

        except FileNotFoundError:
            self.msg_handler.send_message(
                LogEvent(
                    "consensus_service_call",
                    EventType.WARNING,
                    EventScope.CONSENSUS,
                    f"CONSENSUS_SERVICE: Warning: {contract_name} deployment file not found",
                    {"function_name": "_load_contract", "contract_name": contract_name},
                )
            )
            return None
        except json.JSONDecodeError as e:
            self.msg_handler.send_message(
                LogEvent(
                    "consensus_service_call",
                    EventType.ERROR,
                    EventScope.CONSENSUS,
                    f"CONSENSUS_SERVICE: Error decoding {contract_name} deployment file: {str(e)}",
                    {"function_name": "_load_contract", "contract_name": contract_name},
                )
            )
            return None
        except Exception as e:
            self.msg_handler.send_message(
                LogEvent(
                    "consensus_service_call",
                    EventType.ERROR,
                    EventScope.CONSENSUS,
                    f"CONSENSUS_SERVICE: Error loading {contract_name} contract: {str(e)}",
                    {"function_name": "_load_contract", "contract_name": contract_name},
                )
            )
            return None
