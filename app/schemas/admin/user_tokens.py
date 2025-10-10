from pydantic import BaseModel
from app.models.enums import UserTokenType

class UserTokenCreate(BaseModel):
    user_id: int
    type: UserTokenType