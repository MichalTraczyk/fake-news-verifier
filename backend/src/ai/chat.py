from ai.tools.model import get_agent
from ai.tools.schemas import ChatResponse


def generate_reply(history: list[dict]) -> ChatResponse:
    """Stateless: `history` is the whole conversation as [{"role": ..., "content": ...}]."""
    result = get_agent().invoke({"messages": history})
    return result["structured_response"]
