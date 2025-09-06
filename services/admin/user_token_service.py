from fastapi import HTTPException
from models.enums import UserTokenType
from schemas.admin.user_tokens import UserTokenCreate
from repositories.admin.user_token_repository import UserTokenRepository
import secrets
from datetime import datetime, timedelta, UTC

class UserTokenService:
    def __init__(self, repo: UserTokenRepository):
        self.repo = repo

    def create(self, data: UserTokenCreate):
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(UTC) + timedelta(hours=2)

        return self.repo.create({
            'user_id': data.user_id,
            'token': token,
            'type': data.type,
            'expires_at': expires_at
        })

    def getResetPasswordToken(self, token:str):
        user_token = self.repo.findByTokenAndType(token, UserTokenType.RESET_PASSWORD)
        if not user_token or user_token is None:
            raise HTTPException(status_code=404, detail="Token doesn't exists in the database.")

        if datetime.now(UTC) > user_token.expires_at:
            raise HTTPException(status_code=404, detail="Token has expired.")

        return user_token


    def delete(self, id: int):
        return self.repo.delete(id)