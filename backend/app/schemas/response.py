from pydantic import BaseModel, Field


class SourceCitation(BaseModel):
    source: str
    relevance: float | None = None


class TravelResponse(BaseModel):
    answer: str
    summary: str = ""
    accommodation: list[str] = Field(default_factory=list)
    food: list[str] = Field(default_factory=list)
    transport: list[str] = Field(default_factory=list)
    things_to_do: list[str] = Field(default_factory=list)
    budget_summary: list[str] = Field(default_factory=list)
    sources: list[SourceCitation] = Field(default_factory=list)