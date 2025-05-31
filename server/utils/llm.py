from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from server.settings import settings

# chat_llm =  ChatOllama(model="llama3.2")

chat_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=settings.GEMINI_API_KEY,
)