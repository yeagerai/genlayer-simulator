# database/client.py
from os import environ

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()


def get_db_name(database: str) -> str:
    return "genlayer_state" if database == "genlayer" else database


class DBClient:
    def __init__(self, database: str) -> None:
        self.engine = create_engine(
            f"postgresql+psycopg2://{environ.get('DBUSER')}:{environ.get('DBPASSWORD')}@{environ.get('DBHOST')}/{get_db_name(database)}",
            echo=True,
        )

    def get_session(self) -> Session:
        """Return a SQLAlchemy session."""
        return Session(self.engine, expire_on_commit=False)
