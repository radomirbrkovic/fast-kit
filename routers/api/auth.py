from fastapi import HTTPException, status, Form
from models.enums import UserRole
from routers.api.api import public_router as router, translation_manager
from services.auth_service import AuthService

auth_service = AuthService()

@router.post("/login", name='api.auth.authentication')
async def login(email: str = Form(...), password: str = Form(...)):
    result = auth_service.api_authenticate(email, password, UserRole.USER)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translation_manager.gettext('api.auth.invalid_credentials')
        )
    return result


@router.post("/refresh",  name='api.auth.refresh')
def refresh(refresh_token: str = Form(...)):
    result = auth_service.api_refresh_token(refresh_token)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translation_manager.gettext('api.auth.invalid_refresh_token'))
    return result