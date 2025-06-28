from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def welcome():
    return {"message": "Welcome to FastAp, Admin panel developed in FastAPI."}