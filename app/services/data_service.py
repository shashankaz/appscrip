import asyncio

from tavily import TavilyClient

from app.core.config import settings
from app.models.analysis import SourceItem

async def fetch_sector_data(sector: str) -> list[SourceItem]:
    if not settings.tavily_api_key:
        raise ValueError("TAVILY_API_KEY is not set")

    tavily_client = TavilyClient(api_key=settings.tavily_api_key)

    def _search() -> dict:
        return tavily_client.search(
            query=f"{sector} sector India trade opportunities market news",
            topic="news",
            search_depth="basic",
            max_results=5,
            time_range="month",
            include_answer=False,
            include_raw_content=False,
        )

    data = await asyncio.to_thread(_search)

    results: list[SourceItem] = []

    for item in data.get("results", [])[:5]:
        title = (item.get("title") or "").strip()
        link = (item.get("url") or "").strip()
        pub_date = (item.get("published_date") or item.get("date") or "").strip()
        description = (item.get("content") or "").strip()

        if title:
            results.append(
                SourceItem(
                    title=title,
                    link=link or "N/A",
                    published_at=pub_date,
                    summary=description,
                )
            )

    if not results:
        raise ValueError("No recent market data was found for the requested sector.")

    return results
