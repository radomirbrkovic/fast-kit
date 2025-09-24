from typing import List
from schemas.admin.users import UserCreate, UserUpdate, UserOut
from schemas.admin.user_tokens import UserTokenCreate, UserTokenType
from services.admin.base_crud_service import BaseCrudService, ModelType, CreateSchemaType
from services.admin.user_token_service import UserTokenService
from repositories.admin.user_repository import UserRepository
from repositories.admin.user_token_repository import UserTokenRepository
from models.user import Users
from passlib.context import CryptContext
from infastructure.email import send
from routers.admin.admin import templates
from starlette.requests import Request
import secrets
import string
import asyncio

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserService(BaseCrudService[Users, UserCreate, UserUpdate]):
    def __init__(self, repo: UserRepository):
        super().__init__(repo)
        self.request = None

    def set_request(self, request: Request):
        self.request = request

    def get(self, filters: dict = None) -> List[ModelType]:
        users = super().get(filters)
        return [UserOut.model_validate(user) for user in users]

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        result = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        obj_in.hashed_password = bcrypt_context.hash(result)
        user = self.repository.create(obj_in)
        user_token = self._create_user_token_for_reset_password(user_id=user.id)
        self._send_welcome_email(user, result, user_token)
        return user

    def update_password(self, id: str, password: str):
        self.repository.update_password(id,  bcrypt_context.hash(password))

    def _create_user_token_for_reset_password(self, user_id: int):
        user_token_data = UserTokenCreate(user_id=user_id, type=UserTokenType.RESET_PASSWORD)
        user_token_service = UserTokenService(UserTokenRepository(self.repository.getDb()))
        return user_token_service.create(data=user_token_data)

    def _send_welcome_email(self, user, password: str, user_token):
        template = templates.env.get_template('emails/welcome.html')
        asyncio.create_task(send(user.email, "Welcome", template.render({
            'request': self.request,
            'user': user,
            'password': password,
            'url':  self.request.url_for('admin.reset-password.form', token=user_token.token)
        })))