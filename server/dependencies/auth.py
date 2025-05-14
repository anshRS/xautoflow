from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from supabase import Client, ClientOptions, create_client
from server.utils.exceptions import UnauthorizedException
from server.settings import settings
import jwt

security = HTTPBearer()

# Decode and verify JWT manually
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials 
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
        payload = jwt.decode(token, settings.SUPABASE_JWT_SECRET, algorithms=['HS256'], options={'verify_aud': False})
        user_id = payload.get('sub')
        if user_id is None:
            raise UnauthorizedException("Invalid user credentials")
        payload['token'] = token
        return payload        
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token has expired")
    except jwt.PyJWKError:
        raise UnauthorizedException("Invalid auth credentials")

# Supabase client authenticated as the current user
def get_user_supabase_client(user=Depends(get_current_user)) -> Client:
    options = ClientOptions(
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY, options=options)
    return client
