from fastapi import Header, HTTPException, status

from app.core.config import settings

def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    if not settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server authentication is not configured.",
        )

    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )

    return x_api_key
