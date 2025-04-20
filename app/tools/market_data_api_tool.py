from typing import Dict, List
import httpx
from datetime import datetime
from app.core.config import settings

async def get_market_data(
    ticker: str,
    start_date: str,
    end_date: str
) -> Dict:
    """Fetch market data from external API."""
    async with httpx.AsyncClient() as client:
        try:
            headers = {}
            if settings.EXTERNAL_MARKET_DATA_API_KEY:
                headers["Authorization"] = f"Bearer {settings.EXTERNAL_MARKET_DATA_API_KEY}"
            
            response = await client.get(
                settings.EXTERNAL_MARKET_DATA_API_URL,
                params={
                    "symbol": ticker,
                    "from": start_date,
                    "to": end_date
                },
                headers=headers
            )
            response.raise_for_status()
            
            data = response.json()
            return {
                "ticker": ticker,
                "data": [
                    {
                        "date": entry["date"],
                        "open": float(entry["open"]),
                        "high": float(entry["high"]),
                        "low": float(entry["low"]),
                        "close": float(entry["close"]),
                        "volume": int(entry["volume"])
                    }
                    for entry in data["time_series"]
                ]
            }
            
        except httpx.HTTPError as e:
            return {
                "error": f"Market data API error: {str(e)}",
                "ticker": ticker,
                "data": []
            }