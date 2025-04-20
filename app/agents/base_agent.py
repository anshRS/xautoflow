from typing import Dict, Any
from autogen import AssistantAgent, UserProxyAgent
from app.core.llm_client import get_gemini_client

def get_base_llm_config() -> Dict[str, Any]:
    return {
        "config_list": [{
            "model": "gemini-1.5-flash",
            "api_key": get_gemini_client().api_key,
        }],
        "temperature": 0.7,
        "timeout": 600,
        "use_system_prompt": False  # Required for Gemini
    }