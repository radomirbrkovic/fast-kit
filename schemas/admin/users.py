from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional
from models.enums import UserRole
from models.user import Users
from infastructure.database import SessionLocal
import re

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str = Field(min_length=8)
    role: UserRole
    is_active: Optional[bool] = True
    phone_number: Optional[str] = None
    hashed_password: str | None = Field(default=None, exclude=True)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[\W_]", v):
            raise ValueError("Password must contain at least one special character.")
        return v

    @staticmethod
    def validate_unique_email(v, db: SessionLocal):
        if db is None:
            raise ValueError("DB session not provided for uniqueness check.")
        if db.query(Users).filter_by(email=v).first():
            raise ValueError("Email is already in use.")
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None
    phone_number: Optional[str] = None

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