# @title Storage
# @dev Store & retrieve value in a variable
class Storage:
    # @dev Constructor: initializes the storage with 'initial_storage' value
    def __init__(self, initial_storage: str):
        super().__init__()
        self.initial_storage = initial_storage

    # @dev Return the current value of storage
    # @return value of 'self.storage'
    def get_storage(self, fromAddress: str):
        return self.initial_storage

    # @dev Stores the 'new_storage' value in 'self.storage'
    # @param str value to store
    def update_storage(self, fromAddress: str, new_storage: str) -> None:
        self.initial_storage = new_storage
