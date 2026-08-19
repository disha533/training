"""
MCP tool registration, split by whether the tool reads or writes data.

register() is the single entrypoint registry.py calls; it just delegates
to the two sub-modules so callers don't need to know tools got split up.
"""



from fastmcp import FastMCP

from expense_manager_mcp.services import ExpenseService
from expense_manager_mcp.tools import read_tools, write_tools


def register(mcp: FastMCP, service: ExpenseService) -> None:
    read_tools.register(mcp, service)
    write_tools.register(mcp, service)
