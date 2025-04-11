from fastapi import FastAPI
from .routers import auth

app = FastAPI()

app.include_router(auth.router)

@app.get("/", status_code=200)
def root():
    return {"message": "Server Running"}

@app.get("/welcome")
def welcome():
    return {"message": "Email verified successfully. Welcome!"}
