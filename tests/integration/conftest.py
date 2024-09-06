import pytest

from tests.common.request import payload, post_request_localhost
from tests.common.response import has_success_status


@pytest.fixture
def setup_validators():
    result = post_request_localhost(
        payload("create_random_validators", 5, 8, 12, ["openai"], ["gpt-4o"])
    ).json()
    assert has_success_status(result)

    yield

    delete_validators_result = post_request_localhost(
        payload("delete_all_validators")
    ).json()
    assert has_success_status(delete_validators_result)
