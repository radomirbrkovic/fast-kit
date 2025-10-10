from fastapi import Request, HTTPException, status
import os
from dotenv import load_dotenv
from starlette.middleware.base import BaseHTTPMiddleware

def auth(request: Request):
    if request.session.get('auth_id') is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")


class GlobalContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        app_name = os.getenv("APP_NAME", "FastKit")
        request.state.app_name = app_name

        response = await call_next(request)
        return response