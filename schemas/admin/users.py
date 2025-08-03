from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, ClassVar
from models.enums import UserRole
from models.user import Users
import re

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str  # not hashed yet
    role: UserRole
    is_active: bool
    phone_number: Optional[str] = None

    _db_session: ClassVar = None
    @field_validator('email')
    def validate_unique_email(self, v):
        if self._db_session is None:
            raise ValueError("DB session not set for schema.")
        user = self._db_session.query(Users).filter_by(email=v).first()
        if user:
            raise ValueError("Email is already in use.")
        return v

    @field_validator('password')
    def validate_password_strength(self, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[\W_]", v):
            raise ValueError("Password must contain at least one special character.")
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