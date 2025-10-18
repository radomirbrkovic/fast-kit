from abc import ABC, abstractmethod

class DatabaseStrategy(ABC):
    @abstractmethod
    def get_session(self):
        pass

    @abstractmethod
    def create_all(self):
        pass

    @abstractmethod
    def drop_all(self):
        pass