# tests/e2e/test_storage.py

from tests.common.request import (
    deploy_intelligent_contract,
    call_contract_method,
    payload,
    post_request_localhost,
)
from tests.integration.mocks.log_indexer_get_contract_schema_for_code import (
    log_indexer_contract_schema,
)
from tests.integration.mocks.call_contract_function import (
    call_contract_function_response,
)

from tests.common.response import (
    assert_dict_struct,
    has_success_status,
)

from tests.common.accounts import create_new_account

TOKEN_TOTAL_SUPPLY = 1000
TRANSFER_AMOUNT = 100


def test_log_indexer():
    # Validators Setup
    result = post_request_localhost(
        payload("create_random_validators", 5, 8, 12, ["openai"], None, "gpt-3.5-turbo")
    ).json()
    assert has_success_status(result)

    # Account Setup
    from_account = create_new_account()

    # Get contract schema
    contract_code = open("examples/contracts/log_indexer.py", "r").read()
    result_schema = post_request_localhost(
        payload("get_contract_schema_for_code", contract_code)
    ).json()
    assert has_success_status(result_schema)
    assert_dict_struct(result_schema, log_indexer_contract_schema)

    # Deploy Contract
    call_method_response_deploy, transaction_response_deploy = (
        deploy_intelligent_contract(from_account, contract_code, "{}")
    )
    assert has_success_status(transaction_response_deploy)
    contract_address = call_method_response_deploy["result"]["data"]["contract_address"]

    # ##########################################
    # ##### Get closest vector when empty ######
    # ##########################################
    closest_vector_log_0 = post_request_localhost(
        payload(
            "get_contract_state",
            contract_address,
            "get_closest_vector",
            ["I like mango"],
        )
    ).json()
    assert has_success_status(closest_vector_log_0)
    assert closest_vector_log_0["result"]["data"] is None

    # ########################################
    # ############## Add log 0 ###############
    # ########################################
    _, transaction_response_add_log_0 = call_contract_method(
        from_account,
        contract_address,
        "add_log",
        ["I like to eat mango", 0],
    )
    assert has_success_status(transaction_response_add_log_0)
    assert_dict_struct(transaction_response_add_log_0, call_contract_function_response)

    # ########################################
    # ##### Get closest vector to log 0 ######
    # ########################################
    closest_vector_log_0 = post_request_localhost(
        payload(
            "get_contract_state",
            contract_address,
            "get_closest_vector",
            ["I like mango"],
        )
    ).json()
    assert has_success_status(closest_vector_log_0)
    assert float(closest_vector_log_0["result"]["data"]["similarity"]) > 0.86
    assert float(closest_vector_log_0["result"]["data"]["similarity"]) < 0.87

    # ########################################
    # ######### Get log 0 metadata ###########
    # ########################################
    metadata_log_0 = post_request_localhost(
        payload(
            "get_contract_state",
            contract_address,
            "get_vector_metadata",
            [0],
        )
    ).json()
    assert has_success_status(metadata_log_0)
    assert metadata_log_0["result"]["data"] == {"log_id": 0}

    # ########################################
    # ############## Add log 1 ###############
    # ########################################
    _, transaction_response_add_log_1 = call_contract_method(
        from_account,
        contract_address,
        "add_log",
        ["I like carrots", 1],
    )
    assert has_success_status(transaction_response_add_log_1)

    # ########################################
    # ##### Get closest vector to log 1 ######
    # ########################################
    closest_vector_log_1 = post_request_localhost(
        payload(
            "get_contract_state",
            contract_address,
            "get_closest_vector",
            ["I like carrots"],
        )
    ).json()
    assert has_success_status(closest_vector_log_1)
    assert float(closest_vector_log_1["result"]["data"]["similarity"]) == 1

    # ########################################
    # ########### Update log 0 ##############
    # ########################################
    _, transaction_response_update_log_0 = call_contract_method(
        from_account,
        contract_address,
        "update_log",
        [0, "I like to eat a lot of mangoes", 0],
    )
    assert has_success_status(transaction_response_update_log_0)

    # ########################################
    # ###### Get closest vector to log 0 #####
    # ########################################
    closest_vector_log_0_2 = post_request_localhost(
        payload(
            "get_contract_state",
            contract_address,
            "get_closest_vector",
            ["I like mango a lot"],
        )
    ).json()
    assert has_success_status(closest_vector_log_0_2)
    assert float(closest_vector_log_0_2["result"]["data"]["similarity"]) > 0.85
    assert float(closest_vector_log_0_2["result"]["data"]["similarity"]) < 0.86

    # ########################################
    # ########### Remove log 0 ##############
    # ########################################
    _, transaction_response_remove_log_0 = call_contract_method(
        from_account,
        contract_address,
        "remove_log",
        [0],
    )
    assert has_success_status(transaction_response_remove_log_0)

    # ########################################
    # ##### Get closest vector to log 0 ######
    # ########################################
    closest_vector_log_0_3 = post_request_localhost(
        payload(
            "get_contract_state",
            contract_address,
            "get_closest_vector",
            ["I like to eat mango"],
        )
    ).json()
    assert has_success_status(closest_vector_log_0_3)
    assert float(closest_vector_log_0_3["result"]["data"]["similarity"]) > 0.50
    assert float(closest_vector_log_0_3["result"]["data"]["similarity"]) < 0.51

    # ########################################
    # ##### Test id uniqueness after deletion #
    # ########################################

    # Add third log
    _, transaction_response_add_log_2 = call_contract_method(
        from_account,
        contract_address,
        "add_log",
        ["This is the third log", 3],
    )
    assert has_success_status(transaction_response_add_log_2)

    # Check if new item got id 2
    closest_vector_log_2 = post_request_localhost(
        payload(
            "get_contract_state",
            contract_address,
            "get_closest_vector",
            ["This is the third log"],
        )
    ).json()
    assert has_success_status(closest_vector_log_2)
    assert float(closest_vector_log_2["result"]["data"]["similarity"]) > 0.99
    assert closest_vector_log_2["result"]["data"]["id"] == 2
    assert closest_vector_log_2["result"]["data"]["text"] == "This is the third log"
