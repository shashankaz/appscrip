import logging
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Path, status
from app.core.config import settings
from app.services.data_service import fetch_sector_data
from app.services.ai_service import analyze_with_ai
from app.services.report_service import generate_markdown_report
from app.core.rate_limit import enforce_rate_limit
from app.models.analysis import AnalyzeResponse, CachedAnalysis
from app.services.cache_service import get_cached_analysis, set_cached_analysis

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/analyze/{sector}", response_model=AnalyzeResponse)
async def analyze_sector(
    sector: Annotated[
        str,
        Path(
            min_length=2,
            max_length=50,
            pattern=r"^[A-Za-z][A-Za-z\s-]*[A-Za-z]$",
            description="Sector name, such as pharmaceuticals or agriculture.",
        ),
    ],
    session_id: str = Depends(enforce_rate_limit),
):
    try:
        normalized_sector = " ".join(sector.lower().split())
        cached_analysis = get_cached_analysis(normalized_sector)
        if cached_analysis:
            return AnalyzeResponse(report=cached_analysis.report)

        data = await fetch_sector_data(normalized_sector)

        analysis = await analyze_with_ai(normalized_sector, data)

        report = generate_markdown_report(normalized_sector, analysis, len(data))
        set_cached_analysis(
            normalized_sector,
            CachedAnalysis(
                sector=normalized_sector,
                report=report,
                sources=data,
            ),
            settings.cache_ttl_seconds,
        )

        return AnalyzeResponse(report=report)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except httpx.HTTPError as exc:
        logger.exception("External data provider failed.")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to fetch current market data.",
        ) from exc
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unexpected analyze failure.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        ) from exc
