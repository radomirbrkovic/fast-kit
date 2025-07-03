from sqlalchemy.orm import Session
from models.user import Users
from models.enums import UserRole
from passlib.context import CryptContext
from infastructure.Database import SessionLocal


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

data = [
    {
        "email": "super.admin@example.com",
        "first_name": "Super",
        "last_name": "Admin",
        "hashed_password": bcrypt_context.hash("Test123"),
        "role": UserRole.SUPER_ADMIN
    }
]

def run(db: Session):
    print("Seeding users...")
    for user_data in data:
        user = Users(**user_data)
        db.add(user)
    db.commit()
    print("Users seeding complete.")

