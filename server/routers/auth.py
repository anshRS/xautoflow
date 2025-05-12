from fastapi import APIRouter, Depends, status
from server.schemas.auth import UserCreate, UserLogin, UserAuth
from server.controllers.auth import register_user, login_user, get_user 
from server.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(req: UserCreate):
    return register_user(req)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(req: UserLogin):
    return login_user(req)

@router.get("/", status_code=status.HTTP_200_OK)
def get_me(user = Depends(get_current_user)):
    return get_user(user)
