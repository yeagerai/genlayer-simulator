from os import environ
import requests

from database.init_db import clear_db_tables, db_cursor
from rpc.utils import get_rpc_url

from dotenv import load_dotenv
load_dotenv()

db_name = environ.get("DBNAME")


def delete_database():
    connection = db_cursor("postgres")
    cursor = connection.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cursor.close()
    connection.close()

def clear_tables(tables: list):
    clear_db_tables(None, tables)


def test_create_db_endpoint():
    delete_database()
    print(get_rpc_url() + "/create_db")
    response = requests.post(get_rpc_url() + "/create_db", {})
    print(response.text)
    assert response.status_code == 200
    assert response.json()["message"] == f"Database {db_name} created successfully!"