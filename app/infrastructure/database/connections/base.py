from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def get_url(self) -> str:
        pass

    @abstractmethod
    def get_session(self):
        pass

    @abstractmethod
    def create_all(self):
        pass

    @abstractmethod
    def drop_all(self):
        pass