from database.init_db import drop_db_if_it_already_exists
from common.testing.db.base import setup_db_and_tables, db_name
from common.testing.response.base import (
    has_success_status,
    has_data,
    data_is
)
from rpc.tests.base import payload, post_request


def test_create_db_endpoint():
    setup_db_and_tables()
    response = post_request(payload("create_db")).json()
    assert has_success_status(response)
    assert has_data(response)
    assert data_is(response, f'Database {db_name} already exists.')


def test_create_db_endpoint_from_fresh():
    setup_db_and_tables()
    drop_db_if_it_already_exists()
    response = post_request(payload("create_db")).json()
    assert has_success_status(response)
    assert has_data(response)
    assert data_is(response, f'Database {db_name} created successfully.')
