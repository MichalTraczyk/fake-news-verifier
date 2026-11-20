from web.schemas.conversation import Conversation


class ConversationRepository:
    """TODO: swap for postgres"""

    def __init__(self) -> None:
        self._conversations: dict[str, Conversation] = {}

    def save(self, conversation: Conversation) -> Conversation:
        self._conversations[conversation.id] = conversation
        return conversation

    def get(self, conversation_id: str) -> Conversation | None:
        return self._conversations.get(conversation_id)
