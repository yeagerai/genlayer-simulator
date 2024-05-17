import psycopg2

from common.testing.db.base import setup_db_and_tables
from database.init_db import drop_db_if_it_already_exists
from common.testing.db.base import get_all_rows_for_table, all_tables
from common.testing.response.base import (
    has_success_status,
    has_data,
    data_is
)
from rpc.tests.base import payload, post_request


def test_create_tables_endpoint():
    setup_db_and_tables()
    drop_db_if_it_already_exists()

    # Make sure none of the tables exist yet
    for table in all_tables:
        try:
            get_all_rows_for_table(table)
            assert False
        except psycopg2.OperationalError:
            assert True

    post_request(payload("create_db"))
    response = post_request(payload("create_tables")).json()

    assert has_success_status(response)
    assert has_data(response)
    assert data_is(response, "Tables created successfully!")

    # All the tables should exist now
    for table in all_tables:
        try:
            get_all_rows_for_table(table)
            assert True
        except Exception:
            assert False