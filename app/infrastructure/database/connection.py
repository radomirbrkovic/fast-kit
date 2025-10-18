import os
from sqlalchemy.orm import declarative_base

Base = declarative_base()

def get_database_connection():
    driver = os.getenv("DB_DRIVER", "postgres").lower()
    username = os.getenv("DB_USERNAME", "user")
    password = os.getenv("DB_PASSWORD", "password")
    host = os.getenv("DB_HOST", "localhost")
    name = os.getenv("DB_NAME", "fastkit_db")
    port = os.getenv("DB_PORT", "5432")

    if driver == "postgres":
        from app.infrastructure.database.connections.postgres import Postgres
        return Postgres(Base, username, password, host, name, port)
    elif driver == "mysql":
        from app.infrastructure.database.connections.mysql import MySQL
        return MySQL(Base, username, password, host, name, port)
    elif driver == "sqlite":
        from app.infrastructure.database.connections.sqllite import SQLite
        return SQLite(Base, name)
    elif driver == "mongo":
        from app.infrastructure.database.connections.mongo import Mongo
        return Mongo(username, password, host, name, port)
    else:
        raise ValueError(f"Unsupported database driver: {driver}")