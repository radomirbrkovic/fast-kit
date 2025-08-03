from typing import List

from schemas.admin.users import UserCreate, UserUpdate, UserOut
from services.admin.base_crud_service import BaseCrudService, ModelType, CreateSchemaType
from repositories.admin.user_repository import UserRepository
from models.user import Users
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserService(BaseCrudService[Users, UserCreate, UserUpdate]):
    def __init__(self, repo: UserRepository):
        super().__init__(repo)

    def get(self, filters: dict = None) -> List[ModelType]:
        users = super().get(filters)
        return [UserOut.model_validate(user) for user in users]

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in.hashed_password = bcrypt_context.hash(obj_in.password)
        return self.repository.create(obj_in)