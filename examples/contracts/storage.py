from genvm.contracts.base import icontract

# @title Storage
# @dev Store & retrieve value in a variable
@icontract
class Storage:
    
    # @dev Constructor: initializes the storage with 'initial_storage' value
    def __init__(self, initial_storage: str):
        self.storage = initial_storage

    # @dev Return the current value of storage
    # @return value of 'self.storage'
    def get_storage(self):
        return self.storage

    # @dev Stores the 'new_storage' value in 'self.storage'
    # @param str value to store
    def update_storage(self, new_storage: str) -> None:
        self.storage = new_storage  