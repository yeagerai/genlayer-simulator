from backend.node.genvm.icontract import IContract


class MultiTentantStorage(IContract):
    """
    Same functionality as UserStorage, but implemented with multiple storage contracts.
    Each user is assigned to a storage contract, and all storage contracts are managed by this same contract.
    This contract does not prevent users from directly interacting with the storage contracts, but it doesn't bother us for testing purposes.
    This is done to test contract calls between different contracts.
    """

    def __init__(self, storage_contracts: list[str]):
        self.storage_contracts = storage_contracts
        self.mappings = {}  # mapping of user address to storage contract address

    def get_all_storages(self) -> dict[str, str]:
        return {
            storage_contract: Contract(storage_contract).get_storage()
            for storage_contract in self.storage_contracts
        }

    def update_storage(self, new_storage: str) -> None:
        # Assign user to a storage contract if not already assigned
        if contract_runner.from_address not in self.mappings:
            self.mappings[contract_runner.from_address] = self.storage_contracts[0]
            self.storage_contracts = self.storage_contracts[1:]

        contract_to_use = self.mappings[contract_runner.from_address]
        Contract(contract_to_use).update_storage(new_storage)
