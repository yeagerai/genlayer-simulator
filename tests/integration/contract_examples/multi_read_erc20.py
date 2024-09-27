from collections import defaultdict
from backend.node.genvm.icontract import IContract


def default_dict_int():
    return defaultdict(int)


class multi_read_erc20(IContract):
    def __init__(self):

        # address -> contract address -> balance
        self.balances = defaultdict(
            default_dict_int
        )  # TODO: lambdas are not working yet. Once they work, we should `self.balances = defaultdict(lambda: defaultdict(int))`

    def update_token_balances(
        self, account_address: str, token_contracts: list[str]
    ) -> dict[str, int]:
        for token_contract in token_contracts:
            contract = Contract(token_contract)
            balance = contract.get_balance_of(account_address)
            self.balances[account_address][token_contract] = balance

    def get_balances(self) -> dict[str, dict[str, int]]:
        return self.balances
