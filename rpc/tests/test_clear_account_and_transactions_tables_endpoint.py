from database.functions import DatabaseFunctions
from common.testing.db.base import setup_db_and_tables, transaction_data, current_state_data
from rpc.tests.base import (
    payload,
    post_request,
    get_all_rows_for_table
)

tables = ["transactions", "current_state"]


def test_clear_account_and_transactions_tables_endpoint():
    setup_db_and_tables()

    post_request(payload("create_db"))
    post_request(payload("create_tables"))

    with DatabaseFunctions() as dbf:
        dbf.insert_transaction(**transaction_data())
        dbf.insert_current_state(**current_state_data())
        dbf.close()

    for table in tables:
        response = get_all_rows_for_table(table)
        assert len(response) == 1

    result = post_request(payload("clear_account_and_transactions_tables"))
    print(result.json())
    assert result.json()["result"]["status"] == "success"
    assert result.json()["result"]["data"] == "Tables cleared successfully!"

    for table in tables:
        response = get_all_rows_for_table(table)
        assert len(response) == 0