# tests/e2e/test_storage.py
import json

from tests.common.request import (
    deploy_intelligent_contract,
    call_contract_method,
    payload,
    post_request_localhost,
)

from tests.integration.contract_examples.mocks.user_storage_get_contract_schema_for_code import (
    user_storage_contract_schema,
)
from tests.integration.contract_examples.mocks.call_contract_function import (
    call_contract_function_response,
)

from tests.common.response import (
    assert_dict_struct,
    assert_dict_exact,
    has_success_status,
)

from tests.common.accounts import create_new_account
from tests.common.transactions import encode_transaction_data

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
    from_account_a = create_new_account()
    from_account_b = create_new_account()

    # Get contract schema
    contract_code = open("examples/contracts/user_storage.py", "r").read()
    result_schema = post_request_localhost(
        payload("get_contract_schema_for_code", contract_code)
    ).json()
    assert has_success_status(result_schema)
    assert_dict_exact(result_schema, user_storage_contract_schema)

    # Deploy Contract
    # Deploy Contract
    call_method_response_deploy, transaction_response_deploy = (
        deploy_intelligent_contract(from_account_a, contract_code, "{}")
    )

    assert has_success_status(transaction_response_deploy)
    contract_address = call_method_response_deploy["result"]["data"]["contract_address"]

    ########################################
    ######### GET Initial State ############
    ########################################
    params_as_string = json.dumps([])
    encoded_data = encode_transaction_data(["get_complete_storage", params_as_string])
    contract_state_1 = post_request_localhost(
        payload("call", contract_address, from_account_a.address, encoded_data)
    ).json()
    assert has_success_status(contract_state_1)
    assert len(contract_state_1["result"]["data"]) == 0

    ########################################
    ########## ADD User A State ############
    ########################################
    _, transaction_response_call_1 = call_contract_method(
        from_account_a, contract_address, "update_storage", [INITIAL_STATE_USER_A]
    )
    assert has_success_status(transaction_response_call_1)

    # Assert response format
    assert_dict_struct(transaction_response_call_1, call_contract_function_response)

    # Get Updated State
    params_as_string = json.dumps([])
    encoded_data = encode_transaction_data(["get_complete_storage", params_as_string])
    contract_state_2_1 = post_request_localhost(
        payload("call", contract_address, from_account_a.address, encoded_data)
    ).json()
    assert has_success_status(contract_state_2_1)
    assert (
        contract_state_2_1["result"]["data"][from_account_a.address]
        == INITIAL_STATE_USER_A
    )

    # Get Updated State
    params_as_string = json.dumps([from_account_a.address])
    encoded_data = encode_transaction_data(["get_account_storage", params_as_string])
    contract_state_2_2 = post_request_localhost(
        payload(
            "call",
            contract_address,
            from_account_a.address,
            encoded_data,
        )
    ).json()
    assert has_success_status(contract_state_2_2)
    assert contract_state_2_2["result"]["data"] == INITIAL_STATE_USER_A

    ########################################
    ########## ADD User B State ############
    ########################################
    _, transaction_response_call_2 = call_contract_method(
        from_account_b, contract_address, "update_storage", [INITIAL_STATE_USER_B]
    )
    assert has_success_status(transaction_response_call_2)

    # Assert response format
    assert_dict_struct(transaction_response_call_2, call_contract_function_response)

    # Get Updated State
    params_as_string = json.dumps([])
    encoded_data = encode_transaction_data(["get_complete_storage", params_as_string])
    contract_state_3 = post_request_localhost(
        payload("call", contract_address, from_account_a.address, encoded_data)
    ).json()
    assert has_success_status(contract_state_3)
    assert (
        contract_state_3["result"]["data"][from_account_a.address]
        == INITIAL_STATE_USER_A
    )
    assert (
        contract_state_3["result"]["data"][from_account_b.address]
        == INITIAL_STATE_USER_B
    )

    #########################################
    ######### UPDATE User A State ###########
    #########################################
    _, transaction_response_call_3 = call_contract_method(
        from_account_a, contract_address, "update_storage", [UPDATED_STATE_USER_A]
    )
    assert has_success_status(transaction_response_call_3)

    # Assert response format
    assert_dict_struct(transaction_response_call_3, call_contract_function_response)

    # Get Updated State
    params_as_string = json.dumps([])
    encoded_data = encode_transaction_data(["get_complete_storage", params_as_string])
    contract_state_4_1 = post_request_localhost(
        payload("call", contract_address, from_account_a.address, encoded_data)
    ).json()
    assert has_success_status(contract_state_4_1)
    assert (
        contract_state_4_1["result"]["data"][from_account_a.address]
        == UPDATED_STATE_USER_A
    )
    assert (
        contract_state_4_1["result"]["data"][from_account_b.address]
        == INITIAL_STATE_USER_B
    )

    # Get Updated State
    params_as_string = json.dumps([from_account_b.address])
    encoded_data = encode_transaction_data(["get_account_storage", params_as_string])
    contract_state_4_2 = post_request_localhost(
        payload("call", contract_address, from_account_a.address, encoded_data)
    ).json()
    assert has_success_status(contract_state_4_2)
    assert contract_state_4_2["result"]["data"] == INITIAL_STATE_USER_B

    delete_validators_result = post_request_localhost(
        payload("delete_all_validators")
    ).json()
    assert has_success_status(delete_validators_result)
