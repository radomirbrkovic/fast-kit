from sqlalchemy.orm import Session
from passlib.context import CryptContext
from infastructure.Database import SessionLocal
from models.user import Users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.db: Session = SessionLocal()

    def authenticate(self, email: str, password: str, role: str):
        user = self.db.query(Users).filter(Users.email == email).first()

        if not user:
            return None

        if not self.verify_password(password, user.hashed_password):
            return None

        if user.role != role:
            return None

        return user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)