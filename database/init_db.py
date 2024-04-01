import flask
import psycopg2
from os import environ
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from database.credentials import get_orig_db_connection, get_genlayer_db_connection


def db_get_transactions_table_create_command() -> str:
    return """
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        from_address VARCHAR(255),
        to_address VARCHAR(255),
        data JSONB NOT NULL,
        nonce INT,
        value NUMERIC,
        type INT CHECK (type IN (0, 1, 2)),
        gasLimit BIGINT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        final BOOLEAN,
        votes JSONB,
        leader_data JSONB
    )
    """

# types change data internal structure
# 0 -> message
# 1 -> IC_DEPLOY
# 2 -> IC_EXEC
def db_get_current_state_table_create_command() -> str:
    return """
    CREATE TABLE IF NOT EXISTS current_state (
        id VARCHAR(255) PRIMARY KEY,
        state JSONB NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    )
    """

def db_get_validators_table_create_command() -> str:
    return """
    CREATE TABLE IF NOT EXISTS validators (
        id SERIAL PRIMARY KEY,
        stake NUMERIC NOT NULL,
        validator_info JSONB NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    )
    """

def db_cursor(db_name:str) -> psycopg2.extensions.connection:
    if db_name == 'postgres':
        connection = get_orig_db_connection()
    elif db_name == 'genlayer_state':
        connection = get_genlayer_db_connection()
    else:
        raise Exception('options are "postgres" or "genlayer_state"')
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return connection

def create_db_if_it_doesnt_already_exists() -> str:
    new_dbname = environ.get('DBNAME')
    connection = db_cursor('postgres')
    cursor = connection.cursor()
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{new_dbname}'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {new_dbname}")
        result = f"Database {new_dbname} created successfully."
    else:
        result = f"Database {new_dbname} already exists."

    cursor.close()
    connection.close()
    return result


def create_tables_if_they_dont_already_exist(app:flask.app.Flask) -> str:
    table_creation_commands = (
        db_get_transactions_table_create_command(),  # eq to blockchain
        db_get_current_state_table_create_command(),  # eq to eth state trie (type of Merkle Patricia Trie)
        db_get_validators_table_create_command(),  # eq to a smart contract on the rollup with people staking to be validators
    )

    connection = None
    result = "Tables created successfully!"
    try:
        connection = db_cursor('genlayer_state')
        cursor = connection.cursor()

        for command in table_creation_commands:
            cursor.execute(command)

        cursor.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        app.error(error)
        result = 'Failed to create tables!'
    finally:
        if connection is not None:
            connection.close()

    return result
