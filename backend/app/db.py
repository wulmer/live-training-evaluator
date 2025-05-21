import os
from pathlib import Path
from sqlmodel import create_engine

root_path = Path(__file__).parent.parent


def get_db_engine():
    if connection_string := os.getenv("AZURE_SQL_CONNECTION_STRING"):
        engine = create_engine(connection_string)
        return engine
    else:
        return get_sqlite_engine()


def get_sqlite_engine():
    database_url = "sqlite:///database.db"

    connect_args = {"check_same_thread": False}
    engine = create_engine(database_url, connect_args=connect_args)
    return engine
