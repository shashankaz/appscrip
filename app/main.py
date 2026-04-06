from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from app.routes.analyze import router as analyze_router

app = FastAPI(
    title="Trade Opportunities API",
    description="Analyze Indian market sectors and generate markdown trade opportunity reports.",
    version="1.0.0",
)

app.include_router(analyze_router)

app.get("/health", tags=["Health"])(lambda: {"status": "ok"})
