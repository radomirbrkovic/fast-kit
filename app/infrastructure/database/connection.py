import os
from sqlalchemy.orm import declarative_base
from app.infrastructure.database.connections.postgres import Postgres
from app.infrastructure.database.connections.mysql import MySQL
from app.infrastructure.database.connections.sqllite import SQLite
from app.infrastructure.database.connections.mongo import Mongo

Base = declarative_base()

def get_database_connection():
    driver = os.getenv("DB_DRIVER", "postgres").lower()
    username = os.getenv("DB_USERNAME", "user")
    password = os.getenv("DB_PASSWORD", "password")
    host = os.getenv("DB_HOST", "localhost")
    name = os.getenv("DB_NAME", "fastkit_db")
    port = os.getenv("DB_PORT", "5432")

    if driver == "postgres":
        return Postgres(Base, username, password, host, name, port)
    elif driver == "mysql":
        return MySQL(Base, username, password, host, name, port)
    elif driver == "sqlite":
        return SQLite(Base, name)
    elif driver == "mongo":
        return Mongo(username, password, host, name, port)
    else:
        raise ValueError(f"Unsupported database driver: {driver}")