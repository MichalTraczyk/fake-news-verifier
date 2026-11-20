from typing import Literal

from pydantic import BaseModel, Field

from ai.tools.schemas import VerificationResult


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    verification: VerificationResult | None = None


class Conversation(BaseModel):
    id: str
    messages: list[Message] = []


class SendMessageRequest(BaseModel):
    content: str = Field(min_length=1)
