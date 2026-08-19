from fastmcp import Client
from google import genai

from agent_client.client import create_gemini_chat
from agent_client.config import ClientSettings

settings = ClientSettings()

if not settings.gemini_api_key:
    raise RuntimeError("AGENT_GEMINI_API_KEY is not set. Add it to .env")

gemini = genai.Client(api_key=settings.gemini_api_key)

# Single reused chat session. Same behavior as before: created on first use,
# then reused for every subsequent message.
_chat = None


async def get_chat(mcp_client: Client):
    """Create the Gemini chat once, then reuse it for every message after that."""
    global _chat
    if _chat is None:
        _chat = await create_gemini_chat(gemini, mcp_client)
    return _chat
