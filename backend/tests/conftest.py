import os
from collections.abc import Generator
from urllib.parse import urlparse

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

_PG_ENV = ("POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_DB")


@pytest.fixture(scope="session")
def pg_engine() -> Generator[Engine, None, None]:
    with PostgresContainer("postgres:16-alpine", driver="psycopg") as postgres:
        url = postgres.get_connection_url()
        config = Config("alembic.ini")
        config.set_main_option("sqlalchemy.url", url)
        command.upgrade(config, "head")
        engine = create_engine(url)
        # Point get_settings at the testcontainer so direct callers (e.g. the
        # dashboard service) build the same connection string the engine uses.
        parsed = urlparse(url)
        os.environ["POSTGRES_USER"] = parsed.username or ""
        os.environ["POSTGRES_PASSWORD"] = parsed.password or ""
        os.environ["POSTGRES_HOST"] = parsed.hostname or ""
        os.environ["POSTGRES_PORT"] = str(parsed.port or 5432)
        os.environ["POSTGRES_DB"] = parsed.path.lstrip("/")
        get_settings.cache_clear()
        get_settings()
        try:
            yield engine
        finally:
            engine.dispose()
            get_settings.cache_clear()
            for key in _PG_ENV:
                os.environ.pop(key, None)


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
