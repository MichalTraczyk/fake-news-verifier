from typing import Literal

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class Conversation(BaseModel):
    id: str
    messages: list[Message] = []


class SendMessageRequest(BaseModel):
    content: str = Field(min_length=1)
