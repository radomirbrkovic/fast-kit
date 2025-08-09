from pydantic import BaseModel, FutureDate
from models.enums import UserTokenType

class UserTokenCreate(BaseModel):
    user_id: int
    token: str
    type: UserTokenType
    expires_at: FutureDate

class UserTokenUpdate(BaseModel):
    pass

class UserTokenOut(BaseModel):
    pass