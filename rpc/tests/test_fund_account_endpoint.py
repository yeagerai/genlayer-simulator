from common.address import create_new_address
from database.functions import DatabaseFunctions
from common.testing.db.base import (
    setup_db_and_tables,
    get_all_rows_for_table,
    assert_funds_transfer_data_in_db,
    assert_these_tables_are_empty
)
from common.testing.response.base import (
    has_error_status,
    has_success_status,
    has_message,
    has_data,
    message_is,
    data_is
)
from rpc.tests.base import payload, post_request

balance = 10.0


def test_fund_account_endpoint_address_not_in_eth_format():
    setup_db_and_tables()

    assert_these_tables_are_empty(["transactions", "current_state"])

    result = post_request(payload("fund_account", "123", 10.0)).json()

    assert_these_tables_are_empty(["transactions", "current_state"])
 
    assert has_error_status(result)
    assert has_message(result)
    assert message_is(result, "account not in ethereum address format")


def test_fund_account_endpoint_pass_create_account():
    setup_db_and_tables()

    assert_these_tables_are_empty(["transactions", "current_state"])

    result = post_request(payload("fund_account", "create_account", balance)).json()
    print(result)
    all_rows_for_current_state = get_all_rows_for_table("current_state")
    all_rows_for_transactions = get_all_rows_for_table("transactions")
    assert len(all_rows_for_current_state) == 1
    assert len(all_rows_for_transactions) == 1

    address = result["result"]["data"]["address"]

    assert has_success_status(result)
    assert has_data(result)
    assert data_is(result, {"address": address, "balance": balance})

    current_state = all_rows_for_current_state[0]
    
    assert current_state[0] == address
    assert current_state[1] == {"balance": balance}

    transaction = all_rows_for_transactions[0]

    data = {"action":"fund_account", "balance":balance}

    assert_funds_transfer_data_in_db(transaction, address, data, balance)


def test_fund_account_endpoint_account_does_not_exist():
    setup_db_and_tables()

    assert_these_tables_are_empty(["transactions", "current_state"])

    result = post_request(payload("fund_account", create_new_address(), balance)).json()

    all_rows_for_current_state = get_all_rows_for_table("current_state")
    all_rows_for_transactions = get_all_rows_for_table("transactions")
    assert len(all_rows_for_current_state) == 0
    assert len(all_rows_for_transactions) == 0

    assert has_error_status(result)
    assert has_message(result)
    assert message_is(result, "account does not exist")


def test_fund_account_endpoint():
    setup_db_and_tables()

    assert_these_tables_are_empty(["transactions", "current_state"])

    result_create_account = post_request(payload("create_account")).json()
    account = result_create_account["result"]["data"]["address"]
    result = post_request(payload("fund_account", account, balance)).json()

    all_rows_for_current_state = get_all_rows_for_table("current_state")
    all_rows_for_transactions = get_all_rows_for_table("transactions")
    assert len(all_rows_for_current_state) == 1
    assert len(all_rows_for_transactions) == 1

    assert has_success_status(result)
    assert has_data(result)
    assert data_is(result, {"address": account, "balance": balance})

    current_state = all_rows_for_current_state[0]
    
    assert current_state[0] == account
    assert current_state[1] == {"balance": balance}

    transaction = all_rows_for_transactions[0]

    data = {"action":"fund_account", "balance":balance}

    assert_funds_transfer_data_in_db(transaction, account, data, balance)
