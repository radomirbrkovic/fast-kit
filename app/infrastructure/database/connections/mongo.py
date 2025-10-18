from pymongo import MongoClient
from .base import Base

class Mongo(Base):
    def __init__(self, username, password, host, db_name, port):
        uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}"
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def create_all(self):
        pass  # Mongo je schemaless

    def drop_all(self):
        self.client.drop_database(self.db.name)

    def get_session(self):
        return self.db