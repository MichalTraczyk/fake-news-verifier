import uuid

from ai.chat import generate_reply
from web.repositories.conversation_repository import ConversationRepository
from web.schemas.conversation import Conversation, Message


class ConversationService:
    def __init__(self, repository: ConversationRepository) -> None:
        self._repository = repository

    def create(self) -> Conversation:
        return self._repository.create(str(uuid.uuid4()))

    def get(self, conversation_id: str) -> Conversation | None:
        return self._repository.get(conversation_id)

    def send_message(self, conversation_id: str, content: str) -> Message | None:
        if self._repository.get(conversation_id) is None:
            return None

        self._repository.add_message(conversation_id, Message(role="user", content=content))

        conversation = self._repository.get(conversation_id)
        history = [{"role": m.role, "content": m.content} for m in conversation.messages]
        response = generate_reply(history)

        reply = Message(
            role="assistant", content=response.message, verification=response.verification
        )
        return self._repository.add_message(conversation_id, reply)
