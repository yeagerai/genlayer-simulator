# tests/e2e/test_storage.py

import json

from tests.common.request import (
    deploy_intelligent_contract,
    send_transaction,
    payload,
    post_request_localhost,
)
from tests.integration.contract_examples.mocks.llm_erc20_get_contract_schema_for_code import (
    llm_erc20_contract_schema,
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

TOKEN_TOTAL_SUPPLY = 1000
TRANSFER_AMOUNT = 100


def test_llm_erc20():
    # Validators Setup
    result = post_request_localhost(
        payload("create_random_validators", 5, 8, 12, ["openai"], None, "gpt-4o")
    ).json()
    assert has_success_status(result)

    # Account Setup
    from_account_a = create_new_account()
    from_account_b = create_new_account()

    # Get contract schema
    contract_code = open("examples/contracts/llm_erc20.py", "r").read()
    result_schema = post_request_localhost(
        payload("get_contract_schema_for_code", contract_code)
    ).json()
    assert has_success_status(result_schema)
    assert_dict_exact(result_schema, llm_erc20_contract_schema)

    # Deploy Contract
    call_method_response_deploy, transaction_response_deploy = (
        deploy_intelligent_contract(
            from_account_a, contract_code, f'{{"total_supply": "{TOKEN_TOTAL_SUPPLY}"}}'
        )
    )

    assert has_success_status(transaction_response_deploy)
    contract_address = call_method_response_deploy["result"]["data"]["contract_address"]

    ########################################
    ######### GET Initial State ############
    ########################################
    params_as_string = json.dumps([])
    encoded_data = encode_transaction_data(["get_balances", params_as_string])
    contract_state_1 = post_request_localhost(
        payload("call", contract_address, from_account_a.address, encoded_data)
    ).json()
    assert has_success_status(contract_state_1)
    assert contract_state_1["result"]["data"][from_account_a.address] == str(
        TOKEN_TOTAL_SUPPLY
    )

    ########################################
    #### TRANSFER from User A to User B ####
    ########################################
    _, transaction_response_call_1 = send_transaction(
        from_account_a,
        contract_address,
        "transfer",
        [TRANSFER_AMOUNT, from_account_b.address],
    )
    assert has_success_status(transaction_response_call_1)

    # Assert response format
    assert_dict_struct(transaction_response_call_1, call_contract_function_response)

    # Get Updated State
    params_as_string = json.dumps([])
    encoded_data = encode_transaction_data(["get_balances", params_as_string])

    contract_state_2_1 = post_request_localhost(
        payload("call", contract_address, from_account_a.address, encoded_data)
    ).json()
    assert has_success_status(contract_state_2_1)
    assert (
        contract_state_2_1["result"]["data"][from_account_a.address]
        == TOKEN_TOTAL_SUPPLY - TRANSFER_AMOUNT
    )

    assert (
        contract_state_2_1["result"]["data"][from_account_b.address] == TRANSFER_AMOUNT
    )

    # Get Updated State
    params_as_string = json.dumps([from_account_a.address])
    encoded_data = encode_transaction_data(["get_balance_of", params_as_string])
    contract_state_2_2 = post_request_localhost(
        payload(
            "call",
            contract_address,
            from_account_a.address,
            encoded_data,
        )
    ).json()
    assert has_success_status(contract_state_2_2)
    assert contract_state_2_2["result"]["data"] == TOKEN_TOTAL_SUPPLY - TRANSFER_AMOUNT

    # Get Updated State
    params_as_string = json.dumps([from_account_b.address])
    encoded_data = encode_transaction_data(["get_balance_of", params_as_string])
    contract_state_2_3 = post_request_localhost(
        payload(
            "call",
            contract_address,
            from_account_a.address,
            encoded_data,
        )
    ).json()
    assert has_success_status(contract_state_2_3)
    assert contract_state_2_3["result"]["data"] == TRANSFER_AMOUNT

    delete_validators_result = post_request_localhost(
        payload("delete_all_validators")
    ).json()
    assert has_success_status(delete_validators_result)
