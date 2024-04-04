import psycopg2
from os import environ

from dotenv import load_dotenv
load_dotenv()

orig_db_params = {
    "dbname": "postgres",
    "user": environ.get('DBUSER'),
    "password": environ.get('DBPASSWORD'),
    "host": environ.get('DBHOST'),
}


def get_orig_db_connection():
    return psycopg2.connect(**orig_db_params)


genlayer_db_params = {
    "dbname": "genlayer_state",
    "user": environ.get('DBUSER'),
    "password": environ.get('DBPASSWORD'),
    "host": environ.get('DBHOST'),
}


def get_genlayer_db_connection():
    return psycopg2.connect(**genlayer_db_params)
