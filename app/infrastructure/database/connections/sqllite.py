from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base

class SQLite(Base):
    def __init__(self, base, db_name):
        self.base = base
        self.url = f"sqlite:///{db_name}.db"
        self.engine = create_engine(self.url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)

    def get_url(self) -> str:
        return self.url

    def create_all(self):
        self.base.metadata.create_all(self.engine)

    def drop_all(self):
        self.base.metadata.drop_all(self.engine)

    def get_session(self):
        return self.SessionLocal()