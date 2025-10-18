from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.models.enums import UserRole
from app.models.user import Users

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    is_active: Optional[bool] = True
    phone_number: Optional[str] = None
    hashed_password: str | None = Field(default=None, exclude=True)

    @staticmethod
    def validate_unique_email(v, db):
        if db is None:
            raise ValueError("DB session not provided for uniqueness check.")
        if db.query(Users).filter_by(email=v).first():
            raise ValueError("Email is already in use.")
        return v

class UserUpdate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    phone_number: Optional[str] = None

    @staticmethod
    def validate_unique_email(v, id, db):
        if db is None:
            raise ValueError("DB session not provided for uniqueness check.")
        if  db.query(Users).filter(Users.email == v, Users.id != id).first():
            raise ValueError("Email is already in use.")
        return v



class UserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    role: UserRole
    phone_number: Optional[str] = ''

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }

    @property
    def status(self) -> str:
        return "Active" if self.is_active else "Inactive"

    @property
    def role_label(self) -> str:
        return self.role.replace("_", " ").title()