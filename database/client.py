# database/client.py
import psycopg2
from os import environ

from dotenv import load_dotenv

load_dotenv()


def get_database_credentials(database: str) -> str:
    """Retrieve the credentials for a specific database."""
    # Validate database choice and set the appropriate database name
    if database not in ["genlayer", "postgres"]:
        raise ValueError("Invalid database specified")

    db_name = "genlayer_state" if database == "genlayer" else database
    return f"dbname={db_name} user={environ.get('DBUSER')} password={environ.get('DBPASSWORD')} host={environ.get('DBHOST')}"


class PostgresManager:
    def __init__(self, database: str) -> None:
        """Initialize the PostgresManager with connection parameters."""
        database_credentials = get_database_credentials(database)
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 10, database_credentials
        )

    def get_connection(self):
        """Retrieve a connection from the connection pool."""
        return self.connection_pool.getconn()

    def release_connection(self, conn: psycopg2.extensions.connection) -> None:
        """Return a connection to the pool."""
        self.connection_pool.putconn(conn)

    def execute_query(self, query: str, params=None) -> list:
        """Execute a SQL query with optional parameters."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                if cursor.description:
                    return cursor.fetchall()  # Return data for 'SELECT' queries
        except psycopg2.DatabaseError as e:
            conn.rollback()  # Rollback on exceptions
            print(f"Database error: {e}")
            return None
        finally:
            self.release_connection(conn)

    def get(self, table: str, condition: str) -> list:
        """Retrieve rows from a table based on a condition."""
        query = f"SELECT * FROM {table} WHERE {condition}"
        return self.execute_query(query)

    def insert(self, table: str, data_dict: dict) -> None:
        """Insert a dictionary of data into a table."""
        columns = ", ".join(data_dict.keys())
        values = ", ".join(["%s"] * len(data_dict))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self.execute_query(query, list(data_dict.values()))

    def update(self, table: str, data_dict: dict, condition: str) -> None:
        """Update rows in a table based on a condition."""
        set_clause = ", ".join([f"{key} = %s" for key in data_dict])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        self.execute_query(query, list(data_dict.values()))

    def remove(self, table: str, condition: str) -> None:
        """Remove rows from a table based on a condition."""
        query = f"DELETE FROM {table} WHERE {condition}"
        self.execute_query(query)

    def __del__(self) -> None:
        """Close all connections in the pool on destruction of the instance."""
        self.connection_pool.closeall()
