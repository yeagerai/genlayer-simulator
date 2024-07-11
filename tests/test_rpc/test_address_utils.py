# tests/rpc/test_address_utils.py

from rpc.address_utils import create_new_address, address_is_in_correct_format


def test_create_new_address_length():
    address = create_new_address()
    assert len(address) == 42


def test_create_new_address_format():
    address = create_new_address()
    assert address.startswith("0x")
    assert address_is_in_correct_format(address)


def test_address_is_in_correct_format_valid():
    valid_address = "0x" + "a" * 40
    assert address_is_in_correct_format(valid_address)


def test_address_is_in_correct_format_invalid():
    invalid_addresses = [
        "0x" + "z" * 40,  # Invalid character 'z'
        "0x" + "a" * 39,  # Incorrect length
        "1x" + "a" * 40,  # Incorrect prefix
        "0x" + "a" * 41,  # Incorrect length
    ]
    for address in invalid_addresses:
        assert not address_is_in_correct_format(address)
