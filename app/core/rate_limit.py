import time
import uuid
from threading import Lock

from fastapi import Cookie, Depends, HTTPException, Request, Response, status

from app.core.auth import verify_api_key
from app.core.config import settings

request_log: dict[str, list[float]] = {}
request_log_lock = Lock()


def get_or_create_session_id(
    response: Response,
    session_id: str | None = Cookie(default=None, alias=settings.session_cookie_name),
) -> str:
    if session_id:
        return session_id

    new_session_id = str(uuid.uuid4())
    response.set_cookie(
        key=settings.session_cookie_name,
        value=new_session_id,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24,
    )
    return new_session_id


def check_rate_limit(identity: str) -> bool:
    now = time.time()

    with request_log_lock:
        timestamps = request_log.setdefault(identity, [])
        valid_timestamps = [
            timestamp
            for timestamp in timestamps
            if now - timestamp < settings.rate_limit_window_seconds
        ]

        if len(valid_timestamps) >= settings.rate_limit:
            request_log[identity] = valid_timestamps
            return False

        valid_timestamps.append(now)
        request_log[identity] = valid_timestamps
        return True


def enforce_rate_limit(
    request: Request,
    api_key: str = Depends(verify_api_key),
    session_id: str = Depends(get_or_create_session_id),
) -> str:
    identity = f"{api_key}:{session_id}:{request.client.host if request.client else 'unknown'}"

    if not check_rate_limit(identity):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )

    return session_id
