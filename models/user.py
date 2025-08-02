from infastructure.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Enum
from models.enums import *

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole, name="user_role"), nullable=False)
    phone_number = Column(String)