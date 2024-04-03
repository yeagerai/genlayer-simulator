import psycopg2

orig_db_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
}


def get_orig_db_connection():
    return psycopg2.connect(**orig_db_params)


genlayer_db_params = {
    "dbname": "genlayer_state",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
}


def get_genlayer_db_connection():
    return psycopg2.connect(**genlayer_db_params)
