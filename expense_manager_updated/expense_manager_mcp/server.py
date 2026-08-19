from fastmcp import FastMCP

from expense_manager_mcp.config import Settings
from expense_manager_mcp.registry import register_tools


def create_server(settings: Settings | None = None) -> tuple[FastMCP, Settings]:
    app_settings = settings or Settings()
    mcp = FastMCP(app_settings.server_name)
    register_tools(mcp, app_settings)
    return mcp, app_settings
mcp, _settings = create_server()


def main() -> None:
    transport_kwargs: dict = {}
    if _settings.transport in ("http", "streamable-http", "sse"):
        transport_kwargs = {
            "host": _settings.http_host,
            "port": _settings.http_port,
            "path": _settings.http_path,
        }
    mcp.run(transport=_settings.transport, **transport_kwargs)


if __name__ == "__main__":
    main() 