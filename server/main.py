from fastapi import FastAPI
from .routers import auth, profile

app = FastAPI()

app.include_router(auth.router)
app.include_router(profile.router)

@app.get("/", status_code=200)
def root():
    return {"message": "Server Running"}

@app.get("/verify")
def welcome():
    return {"message": "Email verified successfully. Welcome!"}
