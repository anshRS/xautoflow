from typing import Dict, Any
from .base_agent import BaseAssistantAgent, get_base_llm_config
from app.tools.knowledge_tools import query_local_kb
from app.tools.news_api_tool import get_financial_news

RESEARCH_PROMPT = """You are a financial research analyst. Execute specific research tasks using available tools:
1. Query knowledge base for relevant information
2. Fetch and analyze financial news
3. Synthesize findings into clear, actionable insights
Always provide structured, concise results."""

class ResearchAgent(BaseAssistantAgent):
    def __init__(self):
        super().__init__(
            name="ResearchAgent",
            description=RESEARCH_PROMPT,
            llm_config={
                **get_base_llm_config(),
                "functions": [
                    {
                        "name": "query_local_kb",
                        "description": "Query the local knowledge base",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "The search query"
                                }
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "get_financial_news",
                        "description": "Fetch financial news articles",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "The news search query"
                                },
                                "max_results": {
                                    "type": "integer",
                                    "default": 10
                                }
                            },
                            "required": ["query"]
                        }
                    }
                ]
            }
        )
    
    async def synthesize_findings(self, intermediate_results: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize research findings into a coherent summary."""
        prompt = f"""Given the following intermediate research results:
{intermediate_results}

Synthesize these findings into a clear, actionable summary. Include:
1. Key insights
2. Supporting evidence
3. Potential implications
4. Recommended actions"""
        
        response = await self.generate_response(prompt)
        return {"summary": response}

def create_research_agent() -> ResearchAgent:
    return ResearchAgent()