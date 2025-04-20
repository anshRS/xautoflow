from typing import List, Dict
import httpx
from datetime import datetime, timedelta
from app.core.config import settings

async def get_financial_news(
    query: str,
    max_results: int = 10
) -> List[Dict]:
    """Fetch financial news articles."""
    async with httpx.AsyncClient() as client:
        try:
            headers = {}
            if settings.EXTERNAL_NEWS_API_KEY:
                headers["Authorization"] = f"Bearer {settings.EXTERNAL_NEWS_API_KEY}"
            
            response = await client.get(
                settings.EXTERNAL_NEWS_API_URL,
                params={
                    "q": query,
                    "limit": max_results,
                    "from": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
                },
                headers=headers
            )
            response.raise_for_status()
            
            articles = response.json()["articles"]
            return [
                {
                    "title": article["title"],
                    "url": article["url"],
                    "published_at": article["publishedAt"],
                    "source": article["source"]["name"],
                    "snippet": article.get("description", "")
                }
                for article in articles[:max_results]
            ]
            
        except httpx.HTTPError as e:
            return [{
                "error": f"News API error: {str(e)}",
                "query": query
            }]