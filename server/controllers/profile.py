from fastapi import FastAPI, File, UploadFile, Depends
from uuid import uuid4
from datetime import datetime
from urllib.parse import urlparse, unquote
# from server.config.db import supabase
from server.utils.exceptions import BadRequestException

async def update_profile(
        supabase,
        user_id: str,
        name: str,
        avatar: UploadFile = File(None)
):    
    try:
        avatar_url = None

        if avatar:
            # Delete already stored avatar
            res = supabase.table("profiles").select("avatar_url").eq("id", user_id).single().execute()
            current_avatar_path = res.data.get("avatar_url")
            parsed_url = urlparse(current_avatar_path)
            clean_path = parsed_url.path.split("/")[-1]
            clean_path = unquote(clean_path)

            # Store new avatar
            if current_avatar_path:
                supabase.storage.from_("avatars").remove([clean_path])

            ext = avatar.filename.split('.')[-1]
            file_name = f"{uuid4()}.{ext}"

            content = await avatar.read()

            upload_response = supabase.storage.from_('avatars').upload(
                path=file_name, 
                file=content
            )

            # Get public url of the avatar
            avatar_url = supabase.storage.from_('avatars').get_public_url(file_name)        
        
        # Update profiles table
        update_payload = {
            "name": name,
            "updated_at": datetime.now().isoformat()
        }
        if(avatar_url):
            update_payload["avatar_url"] = avatar_url       

        response = (
            supabase.table("profiles")
            .update(update_payload)
            .eq("id", user_id)
            .execute()
        )

        return response

    except Exception as e:
        raise BadRequestException(str(e))