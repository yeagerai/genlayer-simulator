from collections import defaultdict
from backend.node.genvm.icontract import IContract


class read_erc20(IContract):
    def __init__(self, token_contract: str):
        self.balances = defaultdict(int)
        self.token_contract = token_contract

    def get_balance_of(self, account_address: str) -> int:
        contract = Contract(self.token_contract)
        return contract.get_balance_of(account_address)
