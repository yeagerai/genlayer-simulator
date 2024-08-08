# rpc/address_utils.py

from eth_account import Account
from eth_account._utils.validation import is_valid_address

def create_new_address() -> str:
    return Account.create().address


def address_is_in_correct_format(address: str) -> bool:
    return is_valid_address(address)
