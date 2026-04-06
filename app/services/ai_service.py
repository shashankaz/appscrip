import httpx
import logging

from app.core.config import settings
from app.models.analysis import SourceItem

logger = logging.getLogger(__name__)

URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

async def analyze_with_ai(sector: str, data: list[SourceItem]) -> str:
    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set")

    formatted_data = "\n".join(
        [
            (
                f"- Title: {item.title}\n"
                f"  Published: {item.published_at}\n"
                f"  Summary: {item.summary}\n"
                f"  Link: {item.link}"
            )
            for item in data
        ]
    )

    prompt = f"""
    You are analyzing the {sector} sector in India based on current market reporting.

    Use only the supplied source material. Keep the output concise, factual, and structured
    as markdown with these sections:
    ## Executive Summary
    ## Key Trends
    ## Trade Opportunities
    ## Risks
    ## Final Recommendation

    Source material:
    {formatted_data}
    """

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": settings.gemini_api_key,
    }

    async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
        response = await client.post(URL, json=payload, headers=headers)

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.exception("Gemini API request failed: %s", exc.response.text)
        raise ValueError("AI analysis is temporarily unavailable.") from exc

    result = response.json()

    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as exc:
        logger.exception("Unexpected Gemini response format: %s", result)
        raise ValueError("AI analysis returned an invalid response.") from exc
