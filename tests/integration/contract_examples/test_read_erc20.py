import json
import os

from tests.common.request import (
    call_contract_method,
    deploy_intelligent_contract,
    payload,
    post_request_localhost,
)
from tests.common.response import has_success_status


def test_read_erc20(setup_validators, from_account):
    """
    Tests that recursive contract calls work by:
    - creating an LLM ERC20 contract
    - creating a read_erc20 contract that reads the LLM ERC20 contract
    - creating a read_erc20 contract that reads the previous read_erc20 contract

    It's like a linked list, but with contracts.
    """
    TOKEN_TOTAL_SUPPLY = 1000
    current_directory = os.path.dirname(os.path.abspath(__file__))
    contract_file = os.path.join(current_directory, "read_erc20.py")

    # LLM ERC20
    contract_code = open("examples/contracts/llm_erc20.py", "r").read()

    # Deploy Contract
    call_method_response_deploy, transaction_response_deploy = (
        deploy_intelligent_contract(
            from_account,
            contract_code,
            json.dumps({"total_supply": TOKEN_TOTAL_SUPPLY}),
        )
    )
    assert has_success_status(transaction_response_deploy)

    # Read ERC20
    contract_code = open(contract_file, "r").read()

    last_contract_address = call_method_response_deploy["result"]["data"][
        "contract_address"
    ]

    for _ in range(2):
        # deploy contract
        call_method_response_deploy, transaction_response_deploy = (
            deploy_intelligent_contract(
                from_account,
                contract_code,
                json.dumps({"token_contract": last_contract_address}),
            )
        )
        assert has_success_status(transaction_response_deploy)

        last_contract_address = call_method_response_deploy["result"]["data"][
            "contract_address"
        ]

        # check balance
        contract_state = call_contract_method(
            last_contract_address,
            from_account,
            "get_balance_of",
            [from_account.address],
        )
        assert has_success_status(contract_state)
        assert contract_state["result"]["data"] == TOKEN_TOTAL_SUPPLY
