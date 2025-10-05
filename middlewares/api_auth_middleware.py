from fastapi import HTTPException, Request
from infrastructure.jwt_handler import verify_token
from infrastructure.tranaslations import TranslationManager
from models.user import Users
from infrastructure.database import SessionLocal
from models.enums import UserRole

translation_manager = TranslationManager()

def auth(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail=translation_manager.gettext('api.auth.invalid_authorization_token'))

    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail=translation_manager.gettext('api.auth.invalid_token'))

    db = SessionLocal()
    user_id = payload.get("sub")
    user = db.query(Users).filter(Users.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail=translation_manager.gettext('api.auth.user_not_found'))

    request.state.user = user
    request.state.user_role = UserRole(user.role)

    return user