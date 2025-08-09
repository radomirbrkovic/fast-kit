from pydantic import BaseModel, FutureDate
from models.enums import UserTokenType

class UserTokenCreate(BaseModel):
    user_id: int
    type: UserTokenType