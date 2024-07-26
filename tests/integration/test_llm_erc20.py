# tests/e2e/test_storage.py

from tests.common.request import (
    payload,
    post_request_localhost,
    post_request_and_wait_for_finalization,
)
from tests.integration.mocks.llm_erc20_get_contract_schema_for_code import (
    llm_erc20_contract_schema,
)
from tests.integration.mocks.call_contract_function import (
    call_contract_function_response,
)

from tests.common.response import (
    assert_dict_struct,
    has_success_status,
)

TOKEN_TOTAL_SUPPLY = 1000
TRANSFER_AMOUNT = 100


def test_llm_erc20():
    # Validators Setup
    result = post_request_localhost(
        payload("create_random_validators", 5, 8, 12, ["openai"], None, "gpt-4o-mini")
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
    contract_code = open("examples/contracts/llm_erc20.py", "r").read()
    result_schema = post_request_localhost(
        payload("get_contract_schema_for_code", contract_code)
    ).json()
    assert has_success_status(result_schema)
    assert_dict_struct(result_schema, llm_erc20_contract_schema)

    # Deploy Contract
    data = [
        from_address_a,  # from_account
        "LlmErc20",  # class_name
        contract_code,  # contract_code
        f'{{"total_supply": "{TOKEN_TOTAL_SUPPLY}"}}',  # initial_state
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
        payload("get_contract_state", contract_address, "get_balances", [])
    ).json()
    assert has_success_status(contract_state_1)
    assert contract_state_1["result"]["data"][from_address_a] == str(TOKEN_TOTAL_SUPPLY)

    ########################################
    #### TRANSFER from User A to User B ####
    ########################################
    _, transaction_response_call_1 = post_request_and_wait_for_finalization(
        payload(
            "call_contract_function",
            from_address_a,
            contract_address,
            "transfer",
            [TRANSFER_AMOUNT, from_address_b],
        )
    )
    assert has_success_status(transaction_response_call_1)

    # Assert response format
    assert_dict_struct(transaction_response_call_1, call_contract_function_response)

    # Get Updated State
    contract_state_2_1 = post_request_localhost(
        payload("get_contract_state", contract_address, "get_balances", [])
    ).json()
    assert has_success_status(contract_state_2_1)
    assert (
        contract_state_2_1["result"]["data"][from_address_a]
        == TOKEN_TOTAL_SUPPLY - TRANSFER_AMOUNT
    )

    assert contract_state_2_1["result"]["data"][from_address_b] == TRANSFER_AMOUNT

    # Get Updated State
    contract_state_2_2 = post_request_localhost(
        payload(
            "get_contract_state",
            contract_address,
            "get_balance_of",
            [from_address_a],
        )
    ).json()
    assert has_success_status(contract_state_2_2)
    assert contract_state_2_2["result"]["data"] == TOKEN_TOTAL_SUPPLY - TRANSFER_AMOUNT

    # Get Updated State
    contract_state_2_3 = post_request_localhost(
        payload(
            "get_contract_state",
            contract_address,
            "get_balance_of",
            [from_address_b],
        )
    ).json()
    assert has_success_status(contract_state_2_3)
    assert contract_state_2_3["result"]["data"] == TRANSFER_AMOUNT

    delete_validators_result = post_request_localhost(
        payload("delete_all_validators")
    ).json()
    assert has_success_status(delete_validators_result)
