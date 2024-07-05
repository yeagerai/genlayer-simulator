# tests/e2e/test_storage.py

from tests.common.request import (
    payload,
    post_request_localhost,
    post_request_and_wait_for_finalization,
)
from tests.integration.mocks.football_prediction_market_get_contract_schema_for_code import (
    football_prediction_market_contract_schema,
)
from tests.integration.mocks.call_contract_function import (
    call_contract_function_response,
)

from tests.common.response import (
    assert_dict_struct,
    has_success_status,
)


def test_football_prediction_market():
    # Validators Setup
    result = post_request_localhost(
        payload("create_random_validators", 5, 8, 12, ["openai"])
    ).json()
    assert has_success_status(result)

    # Account Setup
    result = post_request_localhost(payload("create_account")).json()
    assert has_success_status(result)
    assert "account_address" in result["result"]["data"]
    from_address_a = result["result"]["data"]["account_address"]

    # Get contract schema
    contract_code = open("examples/contracts/football_prediction_market.py", "r").read()
    result_schema = post_request_localhost(
        payload("get_contract_schema_for_code", contract_code)
    ).json()
    assert has_success_status(result_schema)
    assert_dict_struct(result_schema, football_prediction_market_contract_schema)

    # Deploy Contract
    data = [
        from_address_a,  # from_account
        "LlmErc20",  # class_name
        contract_code,  # contract_code
        f'{{"game_date": "2024-06-26", "team1": "Georgia", "team2": "Portugal"}}',  # initial_state
    ]
    call_method_response_deploy, transaction_response_deploy = (
        post_request_and_wait_for_finalization(
            payload("deploy_intelligent_contract", *data)
        )
    )

    assert has_success_status(transaction_response_deploy)
    contract_address = call_method_response_deploy["result"]["data"]["contract_address"]

    ########################################
    ############# RESOLVE match ############
    ########################################
    _, transaction_response_call_1 = post_request_and_wait_for_finalization(
        payload(
            "call_contract_function",
            from_address_a,
            contract_address,
            "resolve",
            [],
        )
    )
    assert has_success_status(transaction_response_call_1)

    # Assert response format
    assert_dict_struct(transaction_response_call_1, call_contract_function_response)

    delete_validators_result = post_request_localhost(
        payload("delete_all_validators")
    ).json()
    assert has_success_status(delete_validators_result)
