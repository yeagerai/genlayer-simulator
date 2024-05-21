import re
import json
import string
import random
import datetime
import psycopg2

from decimal import Decimal


def create_new_address() -> str:
    new_address = ''.join(random.choice(string.hexdigits) for _ in range(40))
    return '0x' + new_address

def address_is_in_correct_format(address:str) -> bool:
    pattern = r'^0x['+string.hexdigits+']{40}$'
    if re.fullmatch(pattern, address):
        return True
    return False

def error_response(message:str) -> dict:
    return response_format('error', message=message)

def success_response(data) -> dict:
    return response_format('success', data=data)

def response_format(status:str, message:str='', data={}) -> dict:
    return {
        'status': status,
        'message': message,
        'data': data
    }

def db_query_data_to_json(db_cursor:psycopg2.extensions.cursor, db_query_result:dict) -> dict:
    colnames = [desc[0] for desc in db_cursor.description]
    dict_with_names = dict(zip(colnames, db_query_result))
    for k, v in dict_with_names.items():
        if isinstance(v, Decimal):
            dict_with_names[k] = float(v)
    for k, v in dict_with_names.items():
        if isinstance(v, datetime.datetime):
            dict_with_names[k] = str(v.isoformat())
    return json.dumps(dict_with_names)