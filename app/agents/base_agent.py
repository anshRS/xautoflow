from typing import Dict, Any, Optional
from autogen import AssistantAgent, UserProxyAgent
from app.core.config import settings
import google.generativeai as genai

def get_base_llm_config() -> Dict[str, Any]:
    return {
        "config_list": [{
            "model": "gemini-1.5-flash",
            "api_key": settings.GEMINI_API_KEY,
        }],
        "temperature": 0.7,
        "timeout": 600,
        "use_system_prompt": False  # Required for Gemini
    }

class BaseAgent:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def generate_response(self, prompt: str) -> str:
        """Generate a response using the Gemini LLM."""
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Error generating response: {str(e)}"

class BaseAssistantAgent(AssistantAgent, BaseAgent):
    def __init__(self, name: str, description: str, llm_config: Dict[str, Any]):
        super().__init__(name=name, description=description, llm_config=llm_config)
        BaseAgent.__init__(self)

class BaseUserProxyAgent(UserProxyAgent, BaseAgent):
    def __init__(self, name: str, llm_config: Dict[str, Any]):
        super().__init__(name=name, llm_config=llm_config)
        BaseAgent.__init__(self)