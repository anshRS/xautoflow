from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

def get_gemini_client():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.7,
        top_p=0.95,
        top_k=40,
        max_output_tokens=2048,
        convert_system_message_to_human=True
    )