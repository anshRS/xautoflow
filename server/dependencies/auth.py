from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from server.utils.exceptions import UnauthorizedException
from server.config.db import supabase
from server.settings import settings
import jwt

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials 
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
        payload = jwt.decode(token, settings.SUPABASE_JWT_SECRET, algorithms=['HS256'], options={'verify_aud': False})
        user_id = payload.get('sub')
        if user_id is None:
            raise UnauthorizedException("Invalid user credentials")
        return payload        
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token has expired")
    except jwt.PyJWKError:
        raise UnauthorizedException("Invalid auth credentials")