from server.config.db import supabase
from server.schemas.auth import UserCreate, UserLogin
from server.utils.exceptions import BadRequestException
from fastapi import status
from fastapi.responses import JSONResponse
from server.settings import settings

def register_user(data: UserCreate):
    try:
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password,
            "options": {
                "data": {"name": data.name},
                "email_redirect_to": settings.REDIRECT_URL
            }
        })

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"detail": "User created successfully"}
        )
    except Exception as e:
        raise BadRequestException(str(e))

def login_user(data: UserLogin):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })        

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "access_token": response.session.access_token, 
                "id": response.user.id,
                "name": response.user.user_metadata["name"],
                "email": response.user.email,
            }
        )
    except Exception as e:
        raise BadRequestException(str(e))
    