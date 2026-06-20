import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from alembic import command
from alembic.config import Config
from app.core.config import get_settings
from app.core.database import get_db
from app.main import app


@pytest.fixture(scope="session")
def pg_engine() -> Generator[Engine, None, None]:
    with PostgresContainer("postgres:16-alpine", driver="psycopg") as postgres:
        url = postgres.get_connection_url()
        config = Config("alembic.ini")
        config.set_main_option("sqlalchemy.url", url)
        command.upgrade(config, "head")
        engine = create_engine(url)
        # Seed get_settings cache with the testcontainer URL so direct callers work.
        os.environ["DATABASE_URL"] = url
        get_settings.cache_clear()
        get_settings()
        try:
            yield engine
        finally:
            engine.dispose()
            get_settings.cache_clear()
            os.environ.pop("DATABASE_URL", None)


@pytest.fixture()
def db_session(pg_engine: Engine) -> Generator[Session, None, None]:
    connection = pg_engine.connect()
    transaction = connection.begin()
    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
        autoflush=False,
        expire_on_commit=False,
    )
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
