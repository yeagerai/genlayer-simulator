# tests/e2e/test_storage.py

from tests.common.request import (
    payload,
    post_request_localhost,
    post_request_and_wait_for_finalization,
)
from tests.integration.mocks.user_storage_get_contract_schema_for_code import (
    user_storage_contract_schema,
)
from tests.integration.mocks.call_contract_function import (
    call_contract_function_response,
)

from tests.common.response import (
    assert_dict_struct,
    has_success_status,
)

INITIAL_STATE_USER_A = "user_a_initial_state"
UPDATED_STATE_USER_A = "user_a_updated_state"
INITIAL_STATE_USER_B = "user_b_initial_state"
UPDATED_STATE_USER_B = "user_b_updated_state"


def test_user_storage():
    # Validators Setup
    result = post_request_localhost(
        payload("create_random_validators", 10, 8, 12, ["openai"], None, "gpt-4o-mini")
    ).json()
    assert has_success_status(result)

    # Account Setup
    result = post_request_localhost(payload("create_account")).json()
    assert has_success_status(result)
    assert "account_address" in result["result"]["data"]
    from_address_a = result["result"]["data"]["account_address"]

    result = post_request_localhost(payload("create_account")).json()
    assert has_success_status(result)
    assert "account_address" in result["result"]["data"]
    from_address_b = result["result"]["data"]["account_address"]

    # Get contract schema
    contract_code = open("examples/contracts/user_storage.py", "r").read()
    result_schema = post_request_localhost(
        payload("get_contract_schema_for_code", contract_code)
    ).json()
    assert has_success_status(result_schema)
    assert_dict_struct(result_schema, user_storage_contract_schema)

    # Deploy Contract
    data = [
        from_address_a,  # from_account
        "UserStorage",  # class_name
        contract_code,  # contract_code
        "{}",  # constructor_args
    ]
    call_method_response_deploy, transaction_response_deploy = (
        post_request_and_wait_for_finalization(
            payload("deploy_intelligent_contract", *data)
        )
    )

    assert has_success_status(transaction_response_deploy)
    contract_address = call_method_response_deploy["result"]["data"]["contract_address"]

    ########################################
    ######### GET Initial State ############
    ########################################
    contract_state_1 = post_request_localhost(
        payload("get_contract_state", contract_address, "get_complete_storage", [])
    ).json()
    assert has_success_status(contract_state_1)
    assert len(contract_state_1["result"]["data"]) == 0

    ########################################
    ########## ADD User A State ############
    ########################################
    _, transaction_response_call_1 = post_request_and_wait_for_finalization(
        payload(
            "call_contract_function",
            from_address_a,
            contract_address,
            "update_storage",
            [INITIAL_STATE_USER_A],
        )
    )
    assert has_success_status(transaction_response_call_1)

    # Assert response format
    assert_dict_struct(transaction_response_call_1, call_contract_function_response)

    # Get Updated State
    contract_state_2_1 = post_request_localhost(
        payload("get_contract_state", contract_address, "get_complete_storage", [])
    ).json()
    assert has_success_status(contract_state_2_1)
    assert contract_state_2_1["result"]["data"][from_address_a] == INITIAL_STATE_USER_A

    # Get Updated State
    contract_state_2_2 = post_request_localhost(
        payload(
            "get_contract_state",
            contract_address,
            "get_account_storage",
            [from_address_a],
        )
    ).json()
    assert has_success_status(contract_state_2_2)
    assert contract_state_2_2["result"]["data"] == INITIAL_STATE_USER_A

    ########################################
    ########## ADD User B State ############
    ########################################
    _, transaction_response_call_1 = post_request_and_wait_for_finalization(
        payload(
            "call_contract_function",
            from_address_b,
            contract_address,
            "update_storage",
            [INITIAL_STATE_USER_B],
        )
    )
    assert has_success_status(transaction_response_call_1)

    # Assert response format
    assert_dict_struct(transaction_response_call_1, call_contract_function_response)

    # Get Updated State
    contract_state_3 = post_request_localhost(
        payload("get_contract_state", contract_address, "get_complete_storage", [])
    ).json()
    assert has_success_status(contract_state_3)
    assert contract_state_3["result"]["data"][from_address_a] == INITIAL_STATE_USER_A
    assert contract_state_3["result"]["data"][from_address_b] == INITIAL_STATE_USER_B

    #########################################
    ######### UPDATE User A State ###########
    #########################################
    _, transaction_response_call_1 = post_request_and_wait_for_finalization(
        payload(
            "call_contract_function",
            from_address_a,
            contract_address,
            "update_storage",
            [UPDATED_STATE_USER_A],
        )
    )
    assert has_success_status(transaction_response_call_1)

    # Assert response format
    assert_dict_struct(transaction_response_call_1, call_contract_function_response)

    # Get Updated State
    contract_state_4_1 = post_request_localhost(
        payload("get_contract_state", contract_address, "get_complete_storage", [])
    ).json()
    assert has_success_status(contract_state_4_1)
    assert contract_state_4_1["result"]["data"][from_address_a] == UPDATED_STATE_USER_A
    assert contract_state_4_1["result"]["data"][from_address_b] == INITIAL_STATE_USER_B

    # Get Updated State
    contract_state_4_2 = post_request_localhost(
        payload(
            "get_contract_state",
            contract_address,
            "get_account_storage",
            [from_address_b],
        )
    ).json()
    assert has_success_status(contract_state_4_2)
    assert contract_state_4_2["result"]["data"] == INITIAL_STATE_USER_B

    delete_validators_result = post_request_localhost(
        payload("delete_all_validators")
    ).json()
    assert has_success_status(delete_validators_result)
