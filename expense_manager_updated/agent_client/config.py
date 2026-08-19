from pydantic_settings import BaseSettings, SettingsConfigDict


class ClientSettings(BaseSettings):
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    # URL of the MCP server. Start it separately with:
    #   python -m expense_manager_mcp.server
    mcp_server_url: str = "http://127.0.0.1:8000/mcp"

    model_config = SettingsConfigDict(
        env_prefix="AGENT_",
        env_file=".env",
        extra="ignore",
    )
