from fastapi import FastAPI
from routers.admin.auth import router as admin_auth_router

app = FastAPI()

app.include_router(admin_auth_router)

@app.get('/')
async def welcome():
    return {"message": "Welcome to FastAp, Admin panel developed in FastAPI."}