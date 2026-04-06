from pydantic import BaseModel, ConfigDict, Field


class SourceItem(BaseModel):
    title: str = Field(..., min_length=1)
    link: str = Field(..., min_length=1)
    published_at: str = Field(default="")
    summary: str = Field(default="")

    model_config = ConfigDict(str_strip_whitespace=True)


class AnalyzeResponse(BaseModel):
    report: str = Field(..., min_length=1)


class CachedAnalysis(BaseModel):
    sector: str
    report: str
    sources: list[SourceItem]
