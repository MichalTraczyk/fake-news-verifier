from typing import Literal

from pydantic import BaseModel, Field

# OpenAI strict mode requires every field to be present, so optional fields are
# `X | None` without a default - the model sends null instead of omitting them.


class Source(BaseModel):
    url: str
    title: str | None


class VerificationResult(BaseModel):
    claim: str = Field(description="The exact claim that was checked")
    verdict: Literal["true", "false", "misleading", "unverified"]
    confidence: float = Field(description="Number between 0 and 1, e.g. 0.9 for high confidence")
    explanation: str = Field(
        description="2-4 sentences in the user's language; mention the date of the evidence "
        "if the claim is time-sensitive"
    )
    sources: list[Source] = Field(description="Sources you relied on")


class ChatResponse(BaseModel):
    type: Literal["verification", "clarification", "message"] = Field(
        description="'verification' when a claim was checked, 'clarification' when you need "
        "more details from the user, 'message' for anything else"
    )
    message: str = Field(description="The reply shown to the user, in the user's language")
    verification: VerificationResult | None = Field(
        description="Filled when type is 'verification', otherwise null"
    )
