from typing import Protocol

from web.schemas.conversation import Conversation, Message


class ConversationRepository(Protocol):
    """Single source of truth for conversation history.

    To move to Postgres, write a `PostgresConversationRepository` with these methods
    and use it in conversation_controller.py - nothing else changes.
    """

    def create(self, conversation_id: str) -> Conversation: ...

    def get(self, conversation_id: str) -> Conversation | None: ...

    def add_message(self, conversation_id: str, message: Message) -> Message: ...


class InMemoryConversationRepository:
    def __init__(self) -> None:
        self._conversations: dict[str, Conversation] = {}

    def create(self, conversation_id: str) -> Conversation:
        conversation = Conversation(id=conversation_id)
        self._conversations[conversation_id] = conversation
        return conversation

    def get(self, conversation_id: str) -> Conversation | None:
        return self._conversations.get(conversation_id)

    def add_message(self, conversation_id: str, message: Message) -> Message:
        self._conversations[conversation_id].messages.append(message)
        return message
