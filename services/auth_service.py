import asyncio

from sqlalchemy.orm import Session
from fastapi import Request
from passlib.context import CryptContext
from infastructure.database import SessionLocal
from models.enums import UserTokenType
from models.user import Users
from repositories.admin.user_token_repository import UserTokenRepository
from schemas.admin.user_tokens import UserTokenCreate
from services.admin.user_token_service import UserTokenService
from routers.admin.admin import templates
from infastructure.email import send

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.db: Session = SessionLocal()
        self.model = self.db.query(Users)

    def authenticate(self, email: str, password: str, role: str):
        user = self.model.filter(Users.email == email).first()

        if not user:
            return None

        if not self.verify_password(password, user.hashed_password):
            return None

        if user.role != role:
            return None

        return user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # Get authenticated user by session
    def user(self, request: Request):
        if 'auth_id' in request.session:
            user = self.model.filter(Users.id == request.session['auth_id']).first()
            if not user:
                return None
            return user

        return None

    def reset_password(self, email: str, request: Request) -> bool:
        user = self.model.filter(Users.email == email).first()
        if not user:
            return False

        user_token_data = UserTokenCreate(user_id=user.id, type=UserTokenType.RESET_PASSWORD)
        user_token_service = UserTokenService(UserTokenRepository(self.db))
        user_token = user_token_service.create(data=user_token_data)
        self._send_reset_password_email(user, user_token, request)

        return True

    def _send_reset_password_email(self, user, user_token, request):
        template = templates.env.get_template('emails/reset_password.html')
        asyncio.create_task(send(user.email, "Reset Password", template.render({
            'request': request,
            'user': user,
            'url':  request.url_for('admin.reset-password.form', token=user_token.token)
        })))