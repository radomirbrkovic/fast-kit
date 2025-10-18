import asyncio

from sqlalchemy.orm import Session
from fastapi import Request
from passlib.context import CryptContext
from app.infrastructure.database.connection import get_database_connection
from app.models.enums import UserTokenType
from app.models.user import Users
from app.repositories.admin.user_token_repository import UserTokenRepository
from app.schemas.admin.user_tokens import UserTokenCreate
from app.services.admin.user_token_service import UserTokenService
from app.routers.admin.admin import templates
from app.infrastructure.email import send
from app.infrastructure.jwt_handler import create_access_token, create_refresh_token, refresh_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_connection = get_database_connection()

class AuthService:
    def __init__(self):
        self.db: Session = db_connection.get_session()
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

    def api_authenticate(self, email: str, password: str, role: str = "User"):
        user = self.authenticate(email, password, role)
        if not user:
            return None

        token_data = {"sub": str(user.id), "role": user.role.value}

        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        print(pwd_context.verify("password", "$2b$12$h7D7eZVtQY7oyJ0hO2l7ieZ.L0n81qToaWcVDYwcg7WJpwJQtn9gC"))
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

    def api_refresh_token(self, refresh_token: str):
        new_token = refresh_access_token(refresh_token)
        if not new_token:
            return None
        return new_token

    def _send_reset_password_email(self, user, user_token, request):
        template = templates.env.get_template('emails/reset_password.html')
        asyncio.create_task(send(user.email, "Reset Password", template.render({
            'request': request,
            'user': user,
            'url':  request.url_for('admin.reset-password.form', token=user_token.token)
        })))