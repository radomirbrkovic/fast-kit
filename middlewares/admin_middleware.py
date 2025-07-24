from fastapi import Request, HTTPException, status

def auth(request: Request):
    if request.session.get('auth_id') is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")