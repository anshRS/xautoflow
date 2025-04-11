from supabase import create_client, Client
from server.settings import settings

# Initialize Supabase client. The entrypoint to the 
# Supabase functionality and Supabase ecosystem
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)