from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- MCP server ---
    server_name: str = "expense-manager-mcp"
    transport: str = "streamable-http"
    http_host: str = "127.0.0.1"
    http_port: int = 8000
    http_path: str = "/mcp"
    oracle_host: str = "localhost"
    oracle_port: int = 1521
    oracle_service_name: str = "XEPDB1"
    oracle_user: str = "expense_app"
    oracle_password: str = "changeme"

    model_config = SettingsConfigDict(
        env_prefix="EXPENSE_MCP_",
        env_file=".env",
        extra="ignore",
    )
