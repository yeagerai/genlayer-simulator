from database.functions import DatabaseFunctions
from common.testing.db.base import (
    setup_db_and_tables,
    transaction_data,
    current_state_data,
    get_all_rows_for_table
)
from common.testing.response.base import (
    has_success_status,
    has_data,
    data_is
)
from rpc.tests.base import payload, post_request

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

    result = post_request(payload("clear_account_and_transactions_tables")).json()
    assert has_success_status(result)
    assert has_data(result)
    assert data_is(result, "Tables cleared successfully!")

    for table in tables:
        response = get_all_rows_for_table(table)
        assert len(response) == 0