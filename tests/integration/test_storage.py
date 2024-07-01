# tests/e2e/test_storage.py

from tests.common.request import (
    payload,
    post_request_localhost,
    post_request_and_wait_for_finalization,
)
from tests.integration.mocks.storage_get_contract_schema_for_code import (
    storage_contract_schema,
)
from tests.integration.mocks.call_contract_function import (
    call_contract_function_response,
)

from tests.common.response import (
    assert_dict_struct,
    has_success_status,
)

INITIAL_STATE = "a"
UPDATED_STATE = "b"


def test_storage():
    # Validators Setup
    result = post_request_localhost(
        payload("create_random_validators", 10, 8, 12, ["openai"])
    ).json()
    assert has_success_status(result)

    # Account Setup
    result = post_request_localhost(payload("create_account")).json()
    assert has_success_status(result)
    assert "account_address" in result["result"]["data"]
    from_address = result["result"]["data"]["account_address"]
    result = post_request_localhost(payload("fund_account", from_address, 10)).json()
    assert has_success_status(result)

    # Get contract schema
    contract_code = open("examples/contracts/storage.py", "r").read()
    result_schema = post_request_localhost(
        payload("get_contract_schema_for_code", contract_code)
    ).json()
    assert has_success_status(result_schema)
    assert_dict_struct(result_schema, storage_contract_schema)

    # Deploy Contract
    data = [
        from_address,  # from_account
        "Storage",  # class_name
        contract_code,  # contract_code
        f'{{"initial_storage": "{INITIAL_STATE}"}}',  # initial_state
    ]
    call_method_response_deploy, transaction_response_deploy = (
        post_request_and_wait_for_finalization(
            payload("deploy_intelligent_contract", *data)
        )
    )

    assert has_success_status(transaction_response_deploy)
    contract_address = call_method_response_deploy["result"]["data"]["contract_address"]

    # Get Initial State
    contract_state_1 = post_request_localhost(
        payload("get_contract_state", contract_address, "get_storage", [])
    ).json()
    assert has_success_status(contract_state_1)
    assert contract_state_1["result"]["data"] == INITIAL_STATE

    # Update State
    _, transaction_response_call_1 = post_request_and_wait_for_finalization(
        payload(
            "call_contract_function",
            from_address,
            contract_address,
            "update_storage",
            [UPDATED_STATE],
        )
    )
    assert has_success_status(transaction_response_call_1)

    # Assert response format
    assert_dict_struct(transaction_response_call_1, call_contract_function_response)

    # Get Updated State
    contract_state_2 = post_request_localhost(
        payload("get_contract_state", contract_address, "get_storage", [])
    ).json()
    assert has_success_status(contract_state_2)
    assert contract_state_2["result"]["data"] == UPDATED_STATE
