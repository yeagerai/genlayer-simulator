import os
from typing import Iterable

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.database_handler.models import Base


@pytest.fixture
def engine() -> Iterable[Engine]:
    postgres_url = os.getenv("POSTGRES_URL")
    engine = create_engine(postgres_url)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def session(engine: Engine) -> Iterable[Session]:
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    yield session
    session.close()
