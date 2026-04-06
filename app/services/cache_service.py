import time
from threading import Lock

from app.models.analysis import CachedAnalysis

cache_store: dict[str, tuple[float, CachedAnalysis]] = {}
cache_lock = Lock()

def get_cached_analysis(sector: str) -> CachedAnalysis | None:
    now = time.time()

    with cache_lock:
        entry = cache_store.get(sector)
        if not entry:
            return None

        expires_at, cached_analysis = entry
        if now >= expires_at:
            cache_store.pop(sector, None)
            return None

        return cached_analysis


def set_cached_analysis(sector: str, analysis: CachedAnalysis, ttl_seconds: int) -> None:
    with cache_lock:
        cache_store[sector] = (time.time() + ttl_seconds, analysis)
