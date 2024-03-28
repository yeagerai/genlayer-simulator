import psycopg2
from os import environ
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from database.credentials import get_orig_db_connection, get_genlayer_db_connection

new_dbname = environ.get('DBNAME')

connection = get_orig_db_connection()
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()

cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{new_dbname}'")
exists = cursor.fetchone()
if not exists:
    cursor.execute(f"CREATE DATABASE {new_dbname}")
    print(f"Database {new_dbname} created successfully.")
else:
    print(f"Database {new_dbname} already exists.")

cursor.close()
connection.close()

transactions = """
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

current_state = """
CREATE TABLE IF NOT EXISTS current_state (
    id VARCHAR(255) PRIMARY KEY,
    state JSONB NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
"""

validators = """
CREATE TABLE IF NOT EXISTS validators (
    id SERIAL PRIMARY KEY,
    stake NUMERIC NOT NULL,
    validator_info JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
"""

table_creation_commands = (
    transactions,  # eq to blockchain
    current_state,  # eq to eth state trie (type of Merkle Patricia Trie)
    validators,  # eq to a smart contract on the rollup with people staking to be validators
)

connection = None
try:
    connection = get_genlayer_db_connection()
    cursor = connection.cursor()

    for command in table_creation_commands:
        cursor.execute(command)

    cursor.close()
    connection.commit()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if connection is not None:
        connection.close()

print("Database and tables created successfully.")
