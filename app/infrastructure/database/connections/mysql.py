from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base

class MySQL(Base):
    def __init__(self, base, username, password, host, db_name, port):
        self.base = base
        url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}"
        self.engine = create_engine(url)
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)

    def create_all(self):
        self.base.metadata.create_all(self.engine)

    def drop_all(self):
        self.base.metadata.drop_all(self.engine)

    def get_session(self):
        return self.SessionLocal()