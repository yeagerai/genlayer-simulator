from database.init_db import drop_db_if_it_already_exists
from common.testing.db.base import setup_db_and_tables, db_name
from rpc.tests.base import payload, post_request


def test_create_db_endpoint():
    setup_db_and_tables()
    response = post_request(payload("create_db"))
    assert response.status_code == 200
    assert response.json()['result']['status'] == 'success'
    assert response.json()['result']['data'] == f'Database {db_name} already exists.'


def test_create_db_endpoint_from_fresh():
    drop_db_if_it_already_exists()
    response = post_request(payload("create_db"))
    assert response.status_code == 200
    assert response.json()['result']['status'] == 'success'
    assert response.json()['result']['data'] == f'Database {db_name} created successfully.'