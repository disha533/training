from fastmcp import FastMCP

from expense_manager_mcp import tools
from expense_manager_mcp.config import Settings
from expense_manager_mcp.database import create_session_factory
from expense_manager_mcp.services import ExpenseService


def register_tools(mcp: FastMCP, settings: Settings | None = None) -> None:
    settings = settings or Settings()
    session_factory = create_session_factory(settings)
    service = ExpenseService(session_factory)
    tools.register(mcp, service)
