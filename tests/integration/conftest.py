from typing import Iterator
from eth_account import Account
import pytest

from tests.common.accounts import create_new_account
from tests.common.request import payload, post_request_localhost
from tests.common.response import has_success_status


@pytest.fixture
def setup_validators():
    result = post_request_localhost(
        payload("sim_createRandomValidators", 5, 8, 12, ["openai"], ["gpt-4o"])
    ).json()
    assert has_success_status(result)

    yield

    delete_validators_result = post_request_localhost(
        payload("sim_deleteAllValidators")
    ).json()
    assert has_success_status(delete_validators_result)


@pytest.fixture
def from_account() -> Iterator[Account]:
    account = create_new_account()
    yield account
