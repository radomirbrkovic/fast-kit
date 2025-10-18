from pymongo import MongoClient
from .base import Base

class Mongo(Base):
    def __init__(self, username, password, host, db_name, port):
        self.uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}"
        self.client = MongoClient(self.uri)
        self.db = self.client[db_name]

    def get_url(self) -> str:
        return self.uri

    def create_all(self):
        pass  # Mongo je schemaless

    def drop_all(self):
        self.client.drop_database(self.db.name)

    def get_session(self):
        return self.db