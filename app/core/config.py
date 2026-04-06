import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("API_KEY")
    rate_limit: int = int(os.getenv("RATE_LIMIT_REQUESTS"))
    rate_limit_window_seconds: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS"))
    session_cookie_name: str = os.getenv("SESSION_COOKIE_NAME")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY")
    request_timeout_seconds: float = float(os.getenv("REQUEST_TIMEOUT_SECONDS"))
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS"))

settings = Settings()
