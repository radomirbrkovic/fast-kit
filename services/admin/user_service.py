from typing import List

from schemas.admin.users import UserCreate, UserUpdate, UserOut
from schemas.admin.user_tokens import UserTokenCreate, UserTokenType
from services.admin.base_crud_service import BaseCrudService, ModelType, CreateSchemaType
from services.admin.user_token_service import UserTokenService
from repositories.admin.user_repository import UserRepository
from repositories.admin.user_token_repository import UserTokenRepository
from models.user import Users
from passlib.context import CryptContext
import secrets
import string

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserService(BaseCrudService[Users, UserCreate, UserUpdate]):
    def __init__(self, repo: UserRepository):
        super().__init__(repo)

    def get(self, filters: dict = None) -> List[ModelType]:
        users = super().get(filters)
        return [UserOut.model_validate(user) for user in users]

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        result = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        obj_in.hashed_password = bcrypt_context.hash(result)
        user = self.repository.create(obj_in)
        user_token_data = UserTokenCreate(user_id=user.id, type=UserTokenType.RESET_PASSWORD)
        user_token_service = UserTokenService(UserTokenRepository(self.repository.getDb()))
        user_token_service.create(data=user_token_data)
        return user