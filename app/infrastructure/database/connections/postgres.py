from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base

class Postgres(Base):
    def __init__(self, base, username, password, host, db_name, port):
        self.base = base
        self.url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}"
        self.engine = create_engine(self.url)
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)

    def get_url(self) -> str:
        return self.url

    def create_all(self):
        self.base.metadata.create_all(self.engine)

    def drop_all(self):
        self.base.metadata.drop_all(self.engine)

    def get_session(self):
        return self.SessionLocal()