import datetime
import psycopg2

from decimal import Decimal


def convert_to_dict(
    db_cursor: psycopg2.extensions.cursor, db_query_result: dict
) -> dict:
    colnames = [desc[0] for desc in db_cursor.description]
    dict_with_names = dict(zip(colnames, db_query_result))
    for k, v in dict_with_names.items():
        if isinstance(v, Decimal):
            dict_with_names[k] = float(v)
        if isinstance(v, datetime.datetime):
            dict_with_names[k] = str(v.isoformat())
    return dict_with_names
