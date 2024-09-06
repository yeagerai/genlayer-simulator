from tests.common.request import payload, post_request_localhost
from tests.common.response import has_success_status


def test_validators():
    delete_validators_result = post_request_localhost(
        payload("delete_all_validators")
    ).json()
    assert has_success_status(delete_validators_result)

    response = post_request_localhost(payload("create_random_validator", 4)).json()
    assert has_success_status(response)

    validator = response["result"]["data"]
    first_address = validator["address"]

    # Duplicate validator
    response = post_request_localhost(
        payload(
            "create_validator",
            validator["stake"],
            validator["provider"],
            validator["model"],
            validator["config"],
        )
    ).json()
    assert has_success_status(response)

    second_address = response["result"]["data"]["address"]

    # Delete both validators
    response = post_request_localhost(payload("delete_validator", first_address)).json()
    assert has_success_status(response)

    response = post_request_localhost(
        payload("delete_validator", second_address)
    ).json()
    assert has_success_status(response)

    # Check no validators are left

    response = post_request_localhost(payload("get_all_validators")).json()
    assert has_success_status(response)
    assert response["result"]["data"] == []
