from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from server.controllers.profile import update_profile
from server.dependencies.auth import get_user_supabase_client
from typing import Annotated

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.post("/", status_code=status.HTTP_200_OK)
async def update(
    user_id: Annotated[str, Form()],
    name: Annotated[str, Form()],
    avatar: UploadFile = File(None),
    supabase = Depends(get_user_supabase_client)
):
    print(user_id)
    print(name)
    print(avatar)
    
    return await update_profile(supabase, user_id, name, avatar)
