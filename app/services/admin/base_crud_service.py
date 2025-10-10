from typing import Generic, TypeVar, List, Optional
from app.repositories.admin.base import AbstractRepository

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class BaseCrudService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def find(self, id: int) -> Optional[ModelType]:
        return self.repository.find(id)

    def get(self, filters: dict = None) -> List[ModelType]:
        return self.repository.get(filters)

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        return self.repository.create(obj_in)

    def update(self, id: int, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        return self.repository.update(id, obj_in)

    def delete(self, id: int) -> None:
        return self.repository.delete(id)