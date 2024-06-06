from genvm.base.icontract import IContract


# contract class
class UserStorage(IContract):

    # constructor
    def __init__(self):
        self.storage = {}

    # read methods must start with get_
    def get_complete_storage(self):
        return self.storage

    def get_account_storage(self, account_address: str):
        return self.storage[account_address]

    # write method
    def update_storage(self, new_storage: str) -> None:
        self.storage[contract_runner.from_address] = new_storage
