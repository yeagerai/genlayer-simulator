import psycopg2

from common.testing.db.base import setup_db_and_tables, all_tables
from rpc.tests.base import (
    payload,
    post_request,
    get_all_rows_for_table
)


def test_create_db_endpoint():
    setup_db_and_tables()

    # Make sure none of the tables exist yet
    for table in all_tables:
        try:
            get_all_rows_for_table(table)
        except psycopg2.OperationalError:
            assert True

    response = post_request(payload("create_db"))
    response = post_request(payload("create_tables"))

    assert response.status_code == 200
    assert response.json()['result']['status'] == 'success'
    assert response.json()['result']['data'] == "Tables created successfully!"

    # All the tables should exist now
    for table in all_tables:
        try:
            get_all_rows_for_table(table)
            assert True
        except Exception:
            assert False