from fastapi import APIRouter, HTTPException

from web.repositories.conversation_repository import InMemoryConversationRepository
from web.schemas.conversation import Conversation, Message, SendMessageRequest
from web.services.conversation_service import ConversationService

router = APIRouter(prefix="/conversations", tags=["conversations"])

# Swap InMemoryConversationRepository for a Postgres one here.
service = ConversationService(InMemoryConversationRepository())


@router.post("", response_model=Conversation)
def create_conversation():
    return service.create()


@router.get("/{conversation_id}", response_model=Conversation)
def get_conversation(conversation_id: str):
    conversation = service.get(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.post("/{conversation_id}/messages", response_model=Message)
def send_message(conversation_id: str, request: SendMessageRequest):
    reply = service.send_message(conversation_id, request.content)
    if reply is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return reply
