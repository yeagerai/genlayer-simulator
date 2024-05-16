import os
import json
import requests

from database.functions import DatabaseFunctions

from dotenv import load_dotenv
load_dotenv()


def get_all_rows_for_table(table:str):
    with DatabaseFunctions() as db:
        db.cursor.execute(f"SELECT * FROM {table}")
        db.connection.commit()
        transactions = db.cursor.fetchall()
    return transactions


def payload(function_name:str, *args) -> dict:
    return {
        "jsonrpc": "2.0",
        "method": function_name,
        "params": [*args],
        "id": 1,
    }


def post_request(payload:dict):
    return requests.post(
        os.environ['RPCPROTOCOL']+"://"+os.environ['RPCHOST']+":"+os.environ['RPCPORT']+"/api",
        data=json.dumps(payload),
        headers={'Content-Type': 'application/json'}
    )