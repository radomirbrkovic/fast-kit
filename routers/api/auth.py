from fastapi import HTTPException, status, Form
from routers.api.api import public_router as router, translation_manager
from services.auth_service import AuthService

auth_service = AuthService()

@router.post("/login", name='api.authentication')
async def api_login(email: str = Form(...), password: str = Form(...)):
    result = auth_service.api_authenticate(email, password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translation_manager.gettext('api.auth.invalid_credentials')
        )
    return result
