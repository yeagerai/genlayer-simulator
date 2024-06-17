from backend.node.genvm.icontract import IContract


# contract class
class Storage(IContract):

    # constructor
    def __init__(self, initial_storage: str):
        self.storage = initial_storage

    # read methods must start with get_
    def get_storage(self):
        return self.storage

    # write method
    def update_storage(self, new_storage: str) -> None:
        self.storage = new_storage
