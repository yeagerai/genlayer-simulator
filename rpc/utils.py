import re
import string
import random


def create_new_address() -> str:
    new_address = "".join(random.choice(string.hexdigits) for _ in range(40))
    return "0x" + new_address


def address_is_in_correct_format(address: str) -> bool:
    pattern = r"^0x[" + string.hexdigits + "]{40}$"
    if re.fullmatch(pattern, address):
        return True
    return False
