from sqlalchemy.orm import Session
from fastapi import Request
from passlib.context import CryptContext
from infastructure.Database import SessionLocal
from models.user import Users

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