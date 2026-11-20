from typing import Literal

from pydantic import BaseModel, Field

class Source(BaseModel):
    url: str
    title: str | None = None


class VerificationResult(BaseModel):
    claim: str = Field(description="The exact claim that was checked")
    verdict: Literal["true", "false", "misleading", "unverified"]
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str = Field(description="2-4 sentences, in the user's language")
    sources: list[Source]

class ChatResponse(BaseModel):
    type: Literal["verification", "clarification", "message"]
    message: str
    verification: VerificationResult | None = None