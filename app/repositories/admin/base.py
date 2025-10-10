from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, List, Optional

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class AbstractRepository(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    @abstractmethod
    def getDb(self) -> Session:
        pass

    @abstractmethod
    def get(self, filters: dict = None) -> List[ModelType]:
        pass

    @abstractmethod
    def find(self, id: int) -> Optional[ModelType]:
        pass

    @abstractmethod
    def create(self, obj_in: CreateSchemaType) -> ModelType:
        pass

    @abstractmethod
    def update(self, id: int, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass