from pydantic import BaseModel, EmailStr
from typing import Optional
from models.enums import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str  # not hashed yet
    role: UserRole
    is_active: bool
    phone_number: Optional[str] = None

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