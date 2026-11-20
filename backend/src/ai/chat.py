from ai.tools.model import get_agent
from ai.tools.schemas import ChatResponse

# Max agent steps per reply - stops runaway tool-call loops (raises GraphRecursionError)
RECURSION_LIMIT = 25


def generate_reply(history: list[dict]) -> ChatResponse:
    """Stateless: `history` is the whole conversation as [{"role": ..., "content": ...}]."""
    result = get_agent().invoke({"messages": history}, config={"recursion_limit": RECURSION_LIMIT})
    return result["structured_response"]
