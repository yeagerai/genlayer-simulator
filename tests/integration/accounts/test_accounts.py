# tests/e2e/test_storage.py

from tests.common.request import (
    payload,
    post_request_localhost,
    wait_for_transaction,
    send_transaction,
)


from tests.common.response import (
    has_success_status,
    has_error_status,
)

from tests.common.accounts import create_new_account


def test_accounts_funding():
    account = create_new_account()
    new_account_address = account.address

    # Test fund_account
    fund_amount = 1000
    fund_account_result = post_request_localhost(
        payload("fund_account", new_account_address, fund_amount)
    ).json()
    assert has_success_status(fund_account_result)
    assert "transaction_id" in fund_account_result["result"]["data"]
    wait_for_transaction(fund_account_result["result"]["data"]["transaction_id"])

    # Verify balance after funding
    get_balance_after_fund_result = post_request_localhost(
        payload("get_balance", new_account_address)
    ).json()
    assert has_success_status(get_balance_after_fund_result)
    assert (
        get_balance_after_fund_result["result"]["data"]["account_balance"]
        == fund_amount
    )

    # Test fund_account with invalid address
    invalid_address = "0xinvalid_address"
    fund_invalid_account_result = post_request_localhost(
        payload("fund_account", invalid_address, fund_amount)
    ).json()
    assert has_error_status(fund_invalid_account_result)
    print("fund_invalid_account_result", fund_invalid_account_result)

    assert (
        "Incorrect address format. Please provide a valid address."
        in fund_invalid_account_result["result"]["message"]
    )

    # Test get_balance with invalid address
    get_balance_invalid_result = post_request_localhost(
        payload("get_balance", invalid_address)
    ).json()
    assert has_error_status(get_balance_invalid_result)
    assert (
        "Incorrect address format. Please provide a valid address."
        in fund_invalid_account_result["result"]["message"]
    )


def test_accounts_transfers():
    # Setup test accounts
    account_1 = create_new_account()
    account_1_address = account_1.address

    account_2 = create_new_account()
    account_2_address = account_2.address

    fund_amount = 1000
    fund_account_result = post_request_localhost(
        payload("fund_account", account_1_address, fund_amount)
    ).json()
    wait_for_transaction(fund_account_result["result"]["data"]["transaction_id"])

    # Test transfer
    transfer_amount = 200
    _, transaction_response_call_1 = send_transaction(
        account_1, account_2.address, None, None, transfer_amount
    )
    assert has_success_status(transaction_response_call_1)

    # Verify balance after transfer
    get_balance_1_after_transfer = post_request_localhost(
        payload("get_balance", account_1_address)
    ).json()
    assert has_success_status(get_balance_1_after_transfer)
    assert (
        get_balance_1_after_transfer["result"]["data"]["account_balance"]
        == fund_amount - transfer_amount
    )

    get_balance_2_after_transfer = post_request_localhost(
        payload("get_balance", account_2_address)
    ).json()
    assert has_success_status(get_balance_2_after_transfer)
    assert (
        get_balance_2_after_transfer["result"]["data"]["account_balance"]
        == transfer_amount
    )


def test_accounts_burn():
    # Setup test accounts
    account_1 = create_new_account()
    account_1_address = account_1.address

    fund_amount = 1000
    fund_account_result = post_request_localhost(
        payload("fund_account", account_1_address, fund_amount)
    ).json()
    wait_for_transaction(fund_account_result["result"]["data"]["transaction_id"])

    # Test burn
    burn_amount = 200
    _, transaction_response_call_1 = send_transaction(
        account_1, None, None, None, burn_amount
    )
    assert has_success_status(transaction_response_call_1)

    # Verify balance after transfer
    get_balance_1_after_transfer = post_request_localhost(
        payload("get_balance", account_1_address)
    ).json()
    assert has_success_status(get_balance_1_after_transfer)
    assert (
        get_balance_1_after_transfer["result"]["data"]["account_balance"]
        == fund_amount - burn_amount
    )
