from typing import List

from schemas.admin.users import UserCreate, UserUpdate, UserOut
from services.admin.base_crud_service import BaseCrudService, ModelType
from repositories.admin.user_repository import UserRepository
from models.user import Users

class UserService(BaseCrudService[Users, UserCreate, UserUpdate]):
    def __init__(self, repo: UserRepository):
        super().__init__(repo)

    def get(self, filters: dict = None) -> List[ModelType]:
        users = super().get(filters)
        return [UserOut.model_validate(user) for user in users]