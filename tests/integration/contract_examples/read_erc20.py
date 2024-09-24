from backend.node.genvm.contract import Contract
from backend.node.genvm.icontract import IContract

TOKEN_1_CONTRACT_ADDRESS = (
    "0xf6c0589d4ef5ccc5eda8621d8629c9a7ccbfef3bc56209198c16664fceb086ca"
)
TOKEN_2_CONTRACT_ADDRESS = (
    "0x553096d68d63c63116d2ab48b3f59ac0a31ddb0c2c343e59110d37d23415eda6"
)


class read_erc20(IContract):
    def __init__(self):
        pass

    def get_token_balances(self, account_address: str) -> str:
        token_1_contract = Contract(TOKEN_1_CONTRACT_ADDRESS)
        token_1_balance = token_1_contract.get_balace_of(account_address)

        token_2_contract = Contract(TOKEN_2_CONTRACT_ADDRESS)
        token_2_balance = token_2_contract.get_balace_of(account_address)

        return {"token_1": token_1_balance, "token_2": token_2_balance}
