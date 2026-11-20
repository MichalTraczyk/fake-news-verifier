import uuid

from ai.chat import generate_reply
from web.repositories.conversation_repository import ConversationRepository
from web.schemas.conversation import Conversation, Message


class ConversationService:
    def __init__(self, repository: ConversationRepository) -> None:
        self._repository = repository

    def create(self) -> Conversation:
        return self._repository.save(Conversation(id=str(uuid.uuid4())))

    def get(self, conversation_id: str) -> Conversation | None:
        return self._repository.get(conversation_id)

    def send_message(self, conversation_id: str, content: str) -> Message | None:
        conversation = self._repository.get(conversation_id)
        if conversation is None:
            return None

        conversation.messages.append(Message(role="user", content=content))
        history = [m.model_dump() for m in conversation.messages]
        reply = Message(role="assistant", content=generate_reply(history))
        conversation.messages.append(reply)
        self._repository.save(conversation)
        return reply
