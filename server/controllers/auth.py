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
    except Exception as e:
        raise BadRequestException(str(e))

def login_user(data: UserLogin):
    try:
        data = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        }) 

        response = (
            supabase.table("profiles")
            .select("*")
            .eq("id", data.user.id)
            .limit(1)
            .single()
            .execute()
        )        

        response.data["access_token"] = data.session.access_token
        return response
    except Exception as e:
        raise BadRequestException(str(e))

def get_user(user):
    try:
        response = (
            supabase.table("profiles")
            .select("*")
            .eq("id", user["sub"])
            .limit(1)
            .single()
            .execute()
        )
                
        return response
    except Exception as e:
        raise BadRequestException(str(e))
            