from agent_framework_gemini import GeminiChatClient

from config import GEMINI_API_KEY, GEMINI_MODEL


def create_gemini_client() -> GeminiChatClient:
    return GeminiChatClient(
        api_key=GEMINI_API_KEY,
        model=GEMINI_MODEL,
    )
