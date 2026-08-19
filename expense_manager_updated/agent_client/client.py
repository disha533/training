from fastmcp import Client
from google import genai
from google.genai import types

from agent_client.config import ClientSettings

settings = ClientSettings()
SERVER_URL = settings.mcp_server_url


def mcp_tool_to_gemini_declaration(tool) -> types.FunctionDeclaration:
    """Convert an MCP tool's schema into something Gemini understands."""
    return types.FunctionDeclaration(
        name=tool.name,
        description=tool.description or "",
        parameters_json_schema=tool.inputSchema,
    )


def format_tool_output(data) -> dict:
    """MCP tools can return anything; Gemini wants a dict back."""
    if isinstance(data, dict):
        return data
    return {"result": data}


async def create_gemini_chat(gemini: genai.Client, mcp_client: Client):
    """Discover the MCP server's tools and start a Gemini chat that can use them."""
    mcp_tools = await mcp_client.list_tools()
    declarations = [mcp_tool_to_gemini_declaration(t) for t in mcp_tools]
    gemini_tools = types.Tool(function_declarations=declarations)

    return gemini.aio.chats.create(
        model=settings.gemini_model,
        config=types.GenerateContentConfig(tools=[gemini_tools]),
    )
